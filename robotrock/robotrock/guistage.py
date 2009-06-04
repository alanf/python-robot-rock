"""
The stage on which the musicians are added,
moved around, and deleted.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import random
import re

## The following are some contants and things
# that I didn't really want to redeclare a lot
# (especially as they are used in print routines)
background_brush = QBrush(Qt.white)
background_pen = QPen(QBrush(Qt.gray), 2.0)
hdist = QPoint(5,0)
vdist = QPoint(0,5)

unfocused_brush = QBrush(Qt.gray)
unfocused_pen = QPen(QBrush(Qt.black), 2.0)

focused_brush = QBrush(Qt.lightGray)
focused_pen = QPen(QBrush(Qt.darkRed), 2.0)

## The following are the margins for the axes:
lbspace = 30 # 30 pixels to the left and bottom
rtspace = 15 # 15 pixels to the right and top
txtspace = 5 # 5 pixels space for text above baseline

mwidget_size = 20


class RRStage(QWidget):
    """
    This is the area on which musician widgets are added,
    moved around, and deleted. It draws the energy/complexity
    axis space, and restricts musician widget movement to within
    that space.
    """
    def __init__(self, guimain):
        super(RRStage, self).__init__()
        #guimain.logger.debug("Creating Stage widget")
        self.__guimain = guimain
        
        self.setMinimumSize(150,150)
        
        self.__mwidgets = []
        self.__resizeTimer = QTimer(self)
        self.__resizeTimer.setInterval(500)
        self.__resizeTimer.setSingleShot(True)
        self.connect(self.__resizeTimer, SIGNAL('timeout()'), self.updateImages)
        
        guimain.stage = self
    
    def add_musician(self, musician):
        """
        Adds a musician to the stage, given a tuple of the type:
        (musician name, constructor function, path to icon)
        
        This is the tuple type returned by CoreController.filterMusicianList()
        
        Informs the CoreController of the new musician (by way of the musician
        widget constructor).
        """
        #self.__guimain.logger.info("Adding musician: %s" % musician)
        #self.__guimain.core.addMusician(musician)
        mwidget = MusicianWidget(musician, self.__guimain, self)
        self.__mwidgets.append(mwidget)
        mwidget.attemptMove(random.randint(lbspace,self.width()-rtspace), random.randint(lbspace,self.height()-rtspace))
        
        mwidget.show()
    
    def remove_musician(self, mwidget):
        """
        Removes the given musician widget from the list
        of all musician widgets.
        IMPORTANT:
          This method does not delete the underlying musician widget,
          nor does it delete the musician from the CoreController.
          
          To delete a musician, call MusicianWidget.close(),
          which will in turn call this method.
        """
        self.__mwidgets.remove(mwidget)
    
    def list_to_str(self):
        return [str(item) for item in self.__mwidgets]
    
    
    def paintEvent(self, event=None):
        """
        Overrides base QWidget paint handler, in order to paint
        the background and axes.
        """
        painter = QPainter(self)
        
        self.paint_background(painter, event)
        self.paint_axes(painter, event)
    
    def paint_background(self, painter, event):
        """
        Paints the stage background, given a QPainter object.
        """
        painter.setBrush(background_brush)
        painter.setPen(background_pen)
        
        area = self.rect().adjusted(1,1,-2,-2)
        painter.drawRect(area)
    
    def paint_axes(self, painter, event):
        """
        Paints the energy/complexity axes, given a QPainter object.
        """
        painter.save()
        
        # bottomRect encloses the space directly below the x axis (energy)
        bottomRect = self.rect().adjusted(lbspace,self.rect().height() - lbspace, -rtspace, -txtspace)
        painter.setPen(Qt.black)
        
        painter.drawText(bottomRect, Qt.AlignHCenter | Qt.AlignBottom, "Energy")
        painter.drawLine(bottomRect.topLeft(), bottomRect.topRight())
        
        painter.drawLine(bottomRect.topRight() + vdist, bottomRect.topRight() - vdist)
        
        # leftRect encloses the space directly to the left of the y axis (complexity)
        leftRect = self.rect().adjusted(txtspace, rtspace, lbspace - self.rect().width(), -lbspace + 1)
        painter.drawLine(leftRect.topRight(), leftRect.bottomRight())
        painter.drawLine(leftRect.topRight() + hdist, leftRect.topRight() - hdist)
        
        # Rotate the painter in order to draw text
        painter.rotate(-90)
        # RotatedLeftRect is the same as leftRect in screen coordinates, but adjusted for
        #  a rotated origin.
        rotatedLeftRect = QRect(-leftRect.height() - leftRect.y(), leftRect.x(), leftRect.height(), leftRect.width())
        
        painter.drawText(rotatedLeftRect, Qt.AlignHCenter | Qt.AlignTop,"Complexity")
        
        # un-rotate the painter
        painter.restore()
    
    def sizeHint(self):
        # default size
        return QSize(600,400)
    
    def mouseReleaseEvent(self, event):
        """
        Overrides default QWidget method to defocus musician widgets
        if the user clicks on an empty place on the stage.
        """
        event.accept()
        #self.__guimain.logger.debug("Stage clicked at: %d, %d" % (event.x(), event.y()))
        mwidget = self.__guimain.focused_musician
        if mwidget is not None:
            mwidget.clearFocus()
    
    def resizeEvent(self, event):
        """
        Overrides default QWidget.resizeEvent(). Moves all musician widgets with the
        resizing, so that they remain in approximately the same energy/complexity region.
        """
        scaleX = float(event.size().width()) / event.oldSize().width()
        scaleY = float(event.size().height()) / event.oldSize().height()
        
        size = mwidget_size * min([event.size().width(), event.size().height()]) / 100
        
        # Resize timer allows for all musician widgets to resize their icons after
        # a resize occurs. Icons are not updated instantly, in order to reduce
        # computation (as resize events occur frequently when the window is being
        # resized). Instead, icons are updated after the resize timer fires, which
        # resets on each resize event.
        self.__resizeTimer.start()
        
        for mwidget in self.__mwidgets:
            x = (mwidget.x()+mwidget.width()/2) * scaleX
            y = (mwidget.y()+mwidget.height()/2) * scaleY
            
            mwidget.setMinimumSize(size, size)
            mwidget.setMaximumSize(size, size)
            mwidget.attemptMove(x, y)
        
    
    def updateImages(self):
        for mwidget in self.__mwidgets:
            mwidget.updateImageSize()
        
    
    def numMWidgets(self):
        return len(self.__mwidgets)
    

mwidget_count = 0
class MusicianWidget(QWidget):
    """
    A musician widget is the graphical display of a single
    musician object. It contains methods for moving on the
    stage, for custom painting, for being dragged on the stage,
    and for smart deletion.
    """    
    def __init__(self, musician_metadata, guimain, parent):
        """
        Creates a new Musician widget, given a tuple of the type:
        (musician name, constructor function, path to icon).
        Creates the underlying musician object via the constructor,
        and adds it to the CoreController.
        """
        super(MusicianWidget, self).__init__(parent)
        global mwidget_count
        mwidget_count = mwidget_count + 1
        guimain.logger.debug("Musician widget count = %d" % mwidget_count)
        self.num = mwidget_count
        
        #guimain.logger.debug("Creating musician widget")
        
        self.__name = musician_metadata.name
        self.__guimain = guimain
        self.__musician = musician_metadata.constructor()
        self.__stage = parent
        
        self.__energy = 0
        self.__complexity = 0
        
        self.__dragPoint = None
        
        guimain.loadImage(musician_metadata.icon_path, self.__name)
        guimain.core.addMusician(self.__musician)
        
        self.setToolTip("%s" % self.addArticle(self.__name))
        
        size = mwidget_size * min([parent.width(), parent.height()]) / 100
        
        self.setMinimumSize(size,size)
        self.setMaximumSize(size,size)
        
        self.setFocusPolicy(Qt.ClickFocus)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.updateImageSize()
    
    def addArticle(self, noun):
        if re.match("^[aeiou]", noun, re.IGNORECASE) is not None:
            return "An " + noun
        else:
            return "A " + noun
    
    def attemptMove(self, x, y):
        """
        Attempts to move this musician widget to the given coordinates.
        If the coordinates would be outside the allowed area, the widget
        is restricted to the allowed area.
        Changes the underlying musician's energy and complexity to reflect
        the new position.
        """
        validArea = self.__stage.rect().adjusted(lbspace + 1, rtspace, -rtspace, -lbspace+1)
        
        x = int(round(x))
        y = int(round(y))
        
        maxX = validArea.right() - self.width()
        minX = validArea.left()
        maxY = validArea.bottom() - self.height()
        minY = validArea.top()
        
        x = x - self.width()/2
        y = y - self.height()/2
        
        if x > maxX:
            x = maxX
        elif x < minX:
            x = minX
        
        if y > maxY:
            y = maxY
        elif y < minY:
            y = minY
        
        self.energy = 100 * (x - minX) / (maxX - minX)
        self.complexity = 100 + (-100 * (y-minY))/ (maxY - minY)
        
        self.move(x,y)
    
    def getenergy(self):
        return self.__energy
    
    def setenergy(self, energy):
        if energy != self.__energy:
            self.__energy = energy
            self.__musician.energy = energy
            self.emit(SIGNAL("energyChanged"), energy)
            #self.__guimain.logger.debug("set energy to %d" % energy)
    
    def getcomplexity(self):
        return self.__complexity
    
    def setcomplexity(self, complexity):
        if complexity != self.__complexity:
            self.__complexity = complexity
            self.__musician.complexity = complexity
            self.emit(SIGNAL("complexityChanged"), complexity)
            #self.__guimain.logger.debug("set complexity to %d" % complexity)
    
    energy = property(getenergy, setenergy)
    complexity = property(getcomplexity, setcomplexity)
    
    def paintEvent(self, event):
        """
        Overrides QWidget.paintEvent() to allow for custom painting.
        Paints a background, a border, and a custom icon.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.__guimain.focused_musician is not self:
            painter.setBrush(unfocused_brush)
            painter.setPen(unfocused_pen)
        else:
            painter.setBrush(focused_brush)
            painter.setPen(focused_pen)
        
        painter.drawRoundRect(self.rect().adjusted(1,1,-2,-2))
        
        self.paintInstrument(event, painter)
    
    def updateImageSize(self):
        """
        Updates this widget's icon size to reflect its current size.
        """
        inscribed = self.rect().adjusted(10,10,-10,-10)
        self.__guimain.updateImageSize(self.getImageName(), inscribed.size())
        self.update()
    
    def paintInstrument(self, event, painter):
        """
        Paints this widgets custom icon.
        """
        inscribed = self.rect().adjusted(10,10,-10,-10)
        
        painter.drawPixmap(inscribed, self.__guimain.getImage(self.getImageName(), inscribed.size()))
    
    def getImageName(self):
        return self.__name
    
    def mouseReleaseEvent(self, event):
        """
        Overrides QWidget.mouseReleaseEvent() in order to implement
        draggable icons. Closes and deletes this musician if right
        clicked.
        """
        event.accept()
        if event.button() == Qt.RightButton:
            self.close()
        else:
            self.__dragPoint = None
    
    def mouseDoubleClickEvent(self, event):
        """
        Overrides QWidget.mouseDoubleClickEvent(). Moves this
        widget to the back of the stage and deselects it.
        """
        event.accept()
        self.lower()
        self.clearFocus()
    
    def mousePressEvent(self, event):
        """
        Overrides QWidget.mousePressEvent(). Starts a drag if
        clicked with the left mouse button.
        """
        event.accept()
        #self.__guimain.logger.debug("Mouse press: x:%d, y:%d" % (event.x(), event.y()))
        if event.button() == Qt.LeftButton:
            self.__dragPoint = QPoint(event.pos())
    
    def mouseMoveEvent(self, event):
        """
        Overrides QWidget.mouseMoveEvent(). This method is only
        called when a mouse button is down and the mouse is moving.
        Moves this widget with the mouseMoveEvent to implement dragging.
        """
        event.accept()
        if self.__dragPoint is not None:
            #self.__guimain.logger.debug("Mouse move: x:%d\ty:%d" % (event.x(), event.y()))
            #self.__guimain.logger.debug("Drag point is at: x:%d\ty:%d" % (self.__dragPoint.x(), self.__dragPoint.y()))
            deltaX = event.x() - self.__dragPoint.x()
            deltaY = event.y() - self.__dragPoint.y()
            #self.__guimain.logger.debug("DeltaX: %d\tdeltaY:%d" % (deltaX, deltaY))
            self.attemptMove(self.x() + deltaX + self.width()/2, self.y() + deltaY + self.height()/2)
    
    def focusInEvent(self, event):
        event.accept()
        #self.__guimain.logger.debug("Musician widget gained focus")
        self.update()
        self.raise_()
        self.__guimain.focused_musician = self
    
    def focusOutEvent(self, event):
        event.accept()
        #self.__guimain.logger.debug("Musician widget lost focus")
        self.update()
        self.__guimain.unfocusmusician(self)
    
    def closeEvent(self, event):
        self.__guimain.addpanel.enableButton()
        self.__guimain.core.removeMusician(self.__musician)
        self.__stage.remove_musician(self)
        event.accept()
    
    def keyPressEvent(self, event):
        # Key press hander: move if arrow keys, delete if delete/backspace key, lose focus if escape key
        if event.key() == Qt.Key_Up:
            self.attemptMove(self.x()+self.width()/2, self.y()+self.height()/2-10)
        elif event.key() == Qt.Key_Down:
            self.attemptMove(self.x()+self.width()/2, self.y()+self.height()/2+10)
        elif event.key() == Qt.Key_Left:
            self.attemptMove(self.x()+self.width()/2-10, self.y()+self.height()/2)
        elif event.key() == Qt.Key_Right:
            self.attemptMove(self.x()+self.width()/2+10, self.y()+self.height()/2)
        elif event.key() == Qt.Key_Escape:
            self.clearFocus()
        elif event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            self.close()
    
    def __str__(self):
        return "MW: %d" % self.num
    
    def __eq__(self, o):
        return self.num == o.num
    
    def __ne__(self, o):
        return not (self == o)

        