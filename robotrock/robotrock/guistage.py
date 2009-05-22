"""
The stage on which the musicians are added, moved around, and deleted.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import random
import re

## The following are some contants and things
# that I didn't really want to redeclare a lot
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
        #self.__guimain.logger.info("Adding musician: %s" % musician)
        self.__guimain.core.addMusician(musician)
        mwidget = MusicianWidget(musician, self.__guimain, self)
        self.__mwidgets.append(mwidget)
        mwidget.attemptMove(random.randint(lbspace,self.width()-rtspace), random.randint(lbspace,self.height()-rtspace))
        
        mwidget.show()
    
    def remove_musician(self, mwidget):
        self.__mwidgets.remove(mwidget)
    
    
    def paintEvent(self, event=None):
        painter = QPainter(self)
        
        self.paint_background(painter, event)
        self.paint_axes(painter, event)
    
    def paint_background(self, painter, event):
        painter.setBrush(background_brush)
        painter.setPen(background_pen)
        
        area = self.rect().adjusted(1,1,-2,-2)
        painter.drawRect(area)
    
    def paint_axes(self, painter, event):
        painter.save()
        bottomRect = self.rect().adjusted(lbspace,self.rect().height() - lbspace, -rtspace, -txtspace)
        painter.setPen(Qt.black)
        
        painter.drawText(bottomRect, Qt.AlignHCenter | Qt.AlignBottom, "Energy")
        painter.drawLine(bottomRect.topLeft(), bottomRect.topRight())
        
        painter.drawLine(bottomRect.topRight() + vdist, bottomRect.topRight() - vdist)
        
        leftRect = self.rect().adjusted(txtspace, rtspace, lbspace - self.rect().width(), -lbspace + 1)
        painter.drawLine(leftRect.topRight(), leftRect.bottomRight())
        painter.drawLine(leftRect.topRight() + hdist, leftRect.topRight() - hdist)
        
        painter.rotate(-90)
        rotatedLeftRect = QRect(-leftRect.height() - leftRect.y(), leftRect.x(), leftRect.height(), leftRect.width())
        
        painter.drawText(rotatedLeftRect, Qt.AlignHCenter | Qt.AlignTop,"Complexity")
        
        painter.restore()
    
    def sizeHint(self):
        return QSize(500,300)
    
    def mouseReleaseEvent(self, event):
        #self.__guimain.logger.debug("Stage clicked at: %d, %d" % (event.x(), event.y()))
        mwidget = self.__guimain.focused_musician
        if mwidget is not None:
            mwidget.attemptMove(event.x(), event.y())
    
    def resizeEvent(self, event):
        scaleX = float(event.size().width()) / event.oldSize().width()
        scaleY = float(event.size().height()) / event.oldSize().height()
        
        size = mwidget_size * min([event.size().width(), event.size().height()]) / 100
        
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
            

class MusicianWidget(QWidget):
    def __init__(self, musician, guimain, parent):
        super(MusicianWidget, self).__init__(parent)
        #guimain.logger.debug("Creating musician widget")
        self.__guimain = guimain
        self.__musician = musician
        self.__stage = parent
        
        self.__energy = 0
        self.__complexity = 0
        
        if re.match("^[aeiou]", musician.instrument) is not None:
            article = "an"
        else:
            article = "a"
        
        self.setToolTip("A musician, playing %s %s" % (article, musician.instrument))
        
        size = mwidget_size * min([parent.width(), parent.height()]) / 100
        
        self.setMinimumSize(size,size)
        self.setMaximumSize(size,size)
        
        self.setFocusPolicy(Qt.ClickFocus)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
    
    def attemptMove(self, x, y):
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
        inscribed = self.rect().adjusted(10,10,-10,-10)
        self.__guimain.updateImageSize(self.getImageName(), inscribed.size())
        self.update()
    
    def paintInstrument(self, event, painter):
        inscribed = self.rect().adjusted(10,10,-10,-10)
        
        painter.drawPixmap(inscribed, self.__guimain.getImage(self.getImageName(), inscribed.size()))
    
    def getImageName(self):
        return "black-guitar-128x128.png"
    
    def mouseReleaseEvent(self, event):
        event.accept()
        #self.__guimain.logger.debug("Musician widget clicked at: %d, %d" % (event.x(), event.y()))
    
    def mouseDoubleClickEvent(self, event):
        event.accept()
        self.lower()
        self.clearFocus()
    
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

        