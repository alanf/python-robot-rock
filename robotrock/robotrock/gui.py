''' gui.py
    Author: Tim Crossley <tjac0@cs.washington.edu>
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *


import warnings
import logging

from corecontroller import CoreController, MINIMUM_TEMPO, MAXIMUM_TEMPO
from musicianstructured import MusicianStructured

try:
    import guiResources
except ImportError:
    print "GUI resources file not found. Please run the following command:\n\tpyrcc4 -o guiResources.py guiResources.qrc"
    import sys
    sys.exit(1)


class RRGuiMain:
    def __init__(self, args, core=None):
        # Maybe do some argument processing here
        self.app = QApplication(args)
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('robotrock.gui')
        
        if core is None:
            warnings.warn("Gui created without core controller, controller actions disabled (GUI only)")
            self.core = CoreControllerDummy(self)
        else:
            self.core = core
        self.mainWindow = RRMainWindow(rrMain=self)
        
    def run(self):
        self.mainWindow.show()
        return self.app.exec_()

class RRMainWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags(), rrMain=None):
        super(RRMainWindow, self).__init__(parent, flags)
        if rrMain is None:
            raise ValueError, "Tried to create main window without gui main class"
            
        self.rrMain = rrMain
        self.setMinimumSize(800,600)
        
        
        # grid is a grid layout, used like a border layout
        # the center has full stretch, all borders do not like to stretch
        #    0  1  2
        # 0  *  *  *
        # 1  *  *  *
        # 2  *  *  *
        self.grid = QGridLayout()
        
        # Play/Pause Button
        self.playButton = PlayButton()
        self.isPlay = True
        self.connect(self.playButton, SIGNAL("clicked(bool)"), self.playPauseHandler)
        self.grid.addWidget(self.playButton, 1, 2, Qt.AlignHCenter | Qt.AlignBottom)
        
        self.tempoSlider = QSlider(Qt.Vertical)
        self.tempoSlider.setMaximumHeight(200)
        self.tempoSlider.setMinimumHeight(200)
        self.tempoSlider.setMinimum(MINIMUM_TEMPO)
        self.tempoSlider.setMaximum(MAXIMUM_TEMPO)
        self.tempoSlider.setTickInterval(10)
        self.connect(self.tempoSlider, SIGNAL('sliderReleased()'), self.tempoHandler)
        
        self.grid.addWidget(self.tempoSlider, 1,2,Qt.AlignHCenter|Qt.AlignVCenter)
        
        
        textbox = QTextEdit()
        textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #expand both directions
        
        #self.grid.addWidget(textbox,1,1)
        self.grid.setColumnStretch(1,1)
        self.grid.setRowStretch(1,1)
        
        self.setLayout(self.grid)
        
        m = MusicianStructured()
        musician1 = MusicianWidget(musician=m, core=self.rrMain.core, parent=self)
        musician1.userMove(200,200)
        musician1.show()
        
        self.trashIcon = DeleteIcon(mp=self)
        self.grid.addWidget(self.trashIcon,2,2)

        
        self.focusedMusician = None
        
    
    def playPauseHandler(self, checked):
        if self.isPlay:
            self.rrMain.core.play()
            self.playButton.setText("Pause")
        else:
            self.rrMain.core.pause()
            self.playButton.setText("Play")
        
        self.isPlay = not self.isPlay
    
    
    def tempoHandler(self):
        self.rrMain.core.setTempo(self.tempoSlider.value())
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            event.accept()
            if not self.focusedMusician is None and self.childAt(event.pos()) is None:
                self.focusedMusician.userMove(event.x(), event.y())
            
    
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            event.accept()
            if self.focusedMusician is None and self.childAt(event.pos()) is None and event.x() < self.width() - 200 and event.y() < self.height() - 100:
                m = MusicianWidget(MusicianStructured(), core=self.rrMain.core, parent=self)
                m.userMove(event.x(), event.y())
                m.show()

class DeleteIcon(QLabel):
    def __init__(self, parent=None, mp=None):
        super(DeleteIcon, self).__init__(parent)
        self.setText("Delete")
        self.setPixmap(QPixmap(":/delete_icon.png").scaled(75,75,Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.setMinimumSize(75,75)
        
        self.musicianPanel = mp
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            event.accept()
            if not self.musicianPanel.focusedMusician is None:
                self.musicianPanel.rrMain.core.removeMusician(self.musicianPanel.focusedMusician.musician)
                MusicianWidget.allMWidgets.remove(self.musicianPanel.focusedMusician)
                
                self.musicianPanel.focusedMusician.close()
                self.musicianPanel.focusedMusician = None
                
                

class MusicianWidget(QLabel):
    
    allMWidgets = []
    
    def __init__(self, musician, core, parent=None):
        super(MusicianWidget, self).__init__(parent)
        self.setMinimumHeight(100)
        self.setMinimumWidth(100)
        
        self.frameStyle = QFrame.Panel
        
        self.setFrameStyle(self.frameStyle | QFrame.Raised)
        self.setLineWidth(2)
        self.setAutoFillBackground(True)
        
        self.setPixmap(QPixmap(":/metronome_icon.png").scaled(100,100,Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.setFocusPolicy(Qt.ClickFocus)
        self.musician = musician
        
        self.core = core
        self.core.addMusician(musician)
        
        self.parent = parent
        MusicianWidget.allMWidgets.append(self)
        
    def userMove(self, x, y):
        if x < 0 or y < 0:
            return # do not allow the move
        if y > self.parent.height() - self.height():
            return
        if x > self.parent.width() - self.width() - 100:
            return
        
        self.x = x
        self.y = y
        self.musician.energy = 100 * x / self.parent.width()
        self.musician.complexity = (100 * (self.parent.height() - y) / self.parent.height())
        
        
        # absolute minimums
        minW = 600
        minH = 400
        self.move(x,y)
        for w in MusicianWidget.allMWidgets:
            w.update()
            if minW < w.x + w.width() + 100: # 100 pixels extra space
                minW = w.x + w.width() + 100
            if minH < w.y + w.height():
                minH = w.y + w.height()
            
        self.parent.setMinimumWidth(minW)
        self.parent.setMinimumHeight(minH)
        self.parent.update()
        
    
    def focusInEvent(self, event):
        self.setFrameStyle(self.frameStyle | QFrame.Sunken)
        self.parent.focusedMusician = self
    
    def focusOutEvent(self, event):
        self.setFrameStyle(self.frameStyle | QFrame.Raised)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.userMove(self.x, self.y-10)
        elif event.key() == Qt.Key_Down:
            self.userMove(self.x, self.y+10)
        elif event.key() == Qt.Key_Left:
            self.userMove(self.x-10, self.y)
        elif event.key() == Qt.Key_Right:
            self.userMove(self.x+10, self.y)
        elif event.key() == Qt.Key_Escape:
            self.parent.focusedMusician = None
            self.clearFocus()
        elif event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            self.parent.focusedMusician = None
            self.core.removeMusician(self.musician)
            MusicianWidget.allMWidgets.remove(self)
            self.close()

class PlayButton(QPushButton):
    def __init__(self, text="Play", parent=None):
        super(PlayButton, self).__init__(text, parent)
    


'''A dummy version of the core controller class. This class has all the the methods from
   the core controller, but they only print an info message'''
class CoreControllerDummy():
    def __init__(self, rrMain):
        self.rrMain = rrMain
    
    def play(self):
        self.rrMain.logger.info("playing...")
    
    def pause(self):
        #Pause the metronome
        self.rrMain.logger.info("pausing")
    
    def halt(self):
        #Halt the metronome
        self.rrMain.logger.info("halting")
    
    
    def setTempo(self, tempo):
        self.rrMain.logger.info("setting tempo to %d" % tempo)
    
    def updateSongInfo(self, key_signature, time_signature):
        #Update the key and time signatures
        self.rrMain.logger.info("updating song info to key: %d\ttime: %d" % (key_signature, time_signature))
    
    
    def addMusician(self, musician):
        self.rrMain.logger.info("adding musician: %s" % musician.__str__())
    
    
    def removeMusician(self, musician):
        self.rrMain.logger.info("removing musician: %s" % musician.__str__())
    
    
    def filterMusicianList(self, tags):
        self.rrMain.logger.info("filter musician list with tags = %s" % tags.__str__())
    


if __name__ == '__main__':
    import sys
    gui = RRGuiMain(args=sys.argv)
    sys.exit(gui.run())

