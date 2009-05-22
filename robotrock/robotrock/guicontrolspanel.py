"""
This module is a set of controls for the RobotRock GUI.
It contains play/pause button, tempo slider, delete icon,
and a key selector.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""


from PyQt4.QtCore import *
from PyQt4.QtGui  import *

"""
A widget containing the play/pause button, tempo slider,
trash icon, and key changer in a vertical layout.
"""
class RRControlsPanel(QWidget):
    def __init__(self, guimain):
        super(RRControlsPanel, self).__init__()
        #guimain.logger.debug("Creating controls widget")
        
        vpanel = QVBoxLayout()
        vpanel.addStretch(1)
        
        vpanel.addWidget(RRKeySelector(guimain), 0, Qt.AlignHCenter)
        vpanel.addWidget(RRTempoSlider(guimain), 0, Qt.AlignHCenter)
        vpanel.addWidget(RRPlayButton(guimain), 0, Qt.AlignHCenter)
        vpanel.addWidget(RRDeleteIcon(guimain), 0, Qt.AlignHCenter)
        
        self.setLayout(vpanel)
        
    


class RRPlayButton(QPushButton):
    playIcon = None
    pauseIcon = None
    
    def __init__(self, guimain):
        super(RRPlayButton, self).__init__()
        #guimain.logger.debug("Creating play/pause button")
        
        if RRPlayButton.playIcon is None:
            RRPlayButton.playIcon = QIcon(guimain.getImage("play_icon.png", QSize(50,50)))
            RRPlayButton.pauseIcon = QIcon(guimain.getImage("pause_icon.png", QSize(50,50)))
        
        self.__guimain = guimain
        self.__playing = False
        
        self.setToolTip("Starts the musician(s)")
        
        self.setIconSize(QSize(50,50))
        self.setIcon(RRPlayButton.playIcon)
        
        self.connect(self, SIGNAL('clicked(bool)'), self.clickHandler)
        
    
    def clickHandler(self, checked):
        if self.__playing:
            self.setIcon(RRPlayButton.playIcon)
            self.__guimain.core.pause()
            self.setToolTip("Starts the musicians(s)")
        else:
            self.setIcon(RRPlayButton.pauseIcon)
            self.__guimain.core.play()
            self.setToolTip("Stops the musicians(s)")
        self.__playing = not self.__playing
    


class RRDeleteIcon(QLabel):
    def __init__(self, guimain):
        super(RRDeleteIcon, self).__init__("Delete Musician")
        #guimain.logger.debug("Creating delete icon")
        
        self.__guimain = guimain
        self.setToolTip("Delete the selected musician")
        
        self.setPixmap(guimain.getImage("delete-128x128.png").scaled(75,75,Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def mouseReleaseEvent(self, event):
        event.accept()
        if self.__guimain.focused_musician is not None:
            self.__guimain.focused_musician.close()

from corecontroller import MAXIMUM_TEMPO, MINIMUM_TEMPO

class RRTempoSlider(QWidget):
    def __init__(self, guimain):
        super(RRTempoSlider, self).__init__()
        #guimain.logger.debug("Creating tempo slider")
        
        self.__guimain = guimain
        
        grid = QGridLayout()
        self.__slider = QSlider(Qt.Horizontal)
        self.__slider.setMaximumWidth(150)
        self.__slider.setMinimum(MINIMUM_TEMPO)
        self.__slider.setMaximum(MAXIMUM_TEMPO)
        self.__slider.setTickInterval(30)
        self.__slider.setTickPosition(QSlider.TicksBelow)
        self.__slider.setValue((MAXIMUM_TEMPO-MINIMUM_TEMPO)/3)
        
        label = QLabel("Tempo:")
        self.__value_label = QLineEdit()
        self.__value_label.setValidator(QIntValidator(MINIMUM_TEMPO, MAXIMUM_TEMPO, self.__value_label))
        self.__value_label.setMaximumWidth(50)
        self.__value_label.setAlignment(Qt.AlignHCenter)
        
        self.connect(self.__slider, SIGNAL('sliderMoved(int)'), self.immediateSliderHandler)
        self.connect(self.__slider, SIGNAL('sliderReleased()'), self.sliderHandler)
        self.connect(self.__value_label, SIGNAL('returnPressed()'), self.lineEditHandler)
        
        grid.addWidget(label, 0,0,Qt.AlignLeft | Qt.AlignBottom)
        grid.addWidget(self.__value_label, 0,1,Qt.AlignRight | Qt.AlignBottom)
        grid.addWidget(self.__slider,1,0,1,2)
        
        self.setLayout(grid)
        
        self.sliderHandler()
        
        self.setToolTip("Adjusts the tempo of the song")
    
    def immediateSliderHandler(self, val):
        self.__value_label.setText(str(val))
    
    def sliderHandler(self):
        val = self.__slider.value()
        self.__guimain.core.setTempo(val)
        self.__value_label.setText(str(val))
    
    def lineEditHandler(self):
        val = int(self.__value_label.text())
        self.__guimain.core.setTempo(val)
        self.__slider.setValue(val)

from songinfo import VALID_KEY, VALID_KEY_TONALITIES, VALID_TIME_NUMERATOR, VALID_TIME_DENOMINATOR

class RRTimeSelector(QWidget):
    def __init__(self, guimain):
        super(RRTimeSelector, self).__init__()
        self.__guimain = guimain
        
    
    def settime(self, time):
        
        
    time = property(fsets=settime)

class RRKeySelector(QWidget):
    def __init__(self, guimain):
        super(RRKeySelector, self).__init__()
        self.__guimain = guimain
        
        self.__key = ('C', 'Major')
        guimain.core.updateKeySignature(self.__key)
        
        convert = lambda c : unicode(c).replace('b', unichr(9837)).replace('#', unichr(9839))
        
        grid = QGridLayout()
        
        keychooser = QComboBox()
        keys = [convert(x) for x in VALID_KEY]
        keys.sort()
        keychooser.addItems(keys)
        keychooser.setCurrentIndex(keys.index(convert(self.__key[0])))
        
        tonalitychooser = QCheckBox("minor")
        
        self.connect(tonalitychooser, SIGNAL('stateChanged(int)'), self.keyChangeHandler)
        self.connect(keychooser, SIGNAL('currentIndexChanged(const QString&)'), self.keyChangeHandler)
        
        
        grid.addWidget(QLabel("<b>Key</b>"),0,0,1,2,Qt.AlignHCenter)
        grid.addWidget(keychooser, 1,0,Qt.AlignHCenter)
        grid.addWidget(tonalitychooser, 1,1,Qt.AlignHCenter)
        
        self.setLayout(grid)
    
    def keyChangeHandler(self, val):
        changed = False
        if type(val) == type(0):
            if val == 2:
                t = 'Minor'
            else:
                t = 'Major'
            self.__key = (self.__key[0], t)
        else:
            k = val.replace(QChar(9837), 'b').replace(QChar(9839), '#')
            self.__key = (str(k), self.__key[1])
        
        self.__guimain.core.updateKeySignature(self.__key)
        
    


        