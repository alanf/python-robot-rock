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
        vpanel.addWidget(RRTimeSelector(guimain), 0, Qt.AlignHCenter)
        
        vpanel.addWidget(RRTempoSlider(guimain), 0, Qt.AlignHCenter)
        vpanel.addWidget(RRPlayButton(guimain), 0, Qt.AlignHCenter)
        
        vpanel.addWidget(RRDeleteIcon(guimain), 0, Qt.AlignHCenter)
        #vpanel.addWidget(TimeSpinBox([100,2,4,3,24,1],guimain), 0, Qt.AlignHCenter)
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
        # Initialize the tempo to 120 beats per minute.
        self.__slider.setValue(120)
        
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
        
        grid = QGridLayout()
        
        self.__num = TimeSpinBox([x for x in VALID_TIME_NUMERATOR], guimain)
        self.__den = TimeSpinBox([x for x in VALID_TIME_DENOMINATOR], guimain)
        
        self.__time = (4,4)
        
        grid.addWidget(QLabel("<b>Time: </b>"), 0,0,2,1,Qt.AlignVCenter | Qt.AlignRight)
        grid.addWidget(self.__num, 0,1,Qt.AlignHCenter)
        grid.addWidget(self.__den, 1,1,Qt.AlignHCenter)
        
        self.connect(self.__num, SIGNAL('valueChanged(int)'), self.updateTime)
        self.connect(self.__den, SIGNAL('valueChanged(int)'), self.updateTime)
        
        self.setLayout(grid)
    
    
    def updateTime(self, val):
        self.time = (self.__num.value(), self.__den.value())
    
    def settime(self, time):
        if self.__time != time:
            self.__guimain.core.updateTimeSignature(time)
            self.__time = time
        
    time = property(fset=settime)

class TimeSpinBox(QSpinBox):
    def __init__(self, values, guimain):
        super(TimeSpinBox, self).__init__()
        
        values.sort()
        self.__values = values
        self.__guimain = guimain
        
        self.__min = min(values) - 1
        self.__max = max(values) + 1
        self.setMinimum(self.__min)
        self.setMaximum(self.__max)
        
        self.__index = self.__values.index(4)
        
        self.updateValue()
    
    def updateValue(self):
        self.setValue(self.__values[self.__index])
    
    def stepBy(self, val):
        self.__index = self.__index + val
        self.setMinimum(self.__min)
        self.setMaximum(self.__max)
        if self.__index == 0:
            self.setMinimum(self.__values[self.__index])
        elif self.__index == len(self.__values) - 1:
            self.setMaximum(self.__values[self.__index])
        self.updateValue()
    
    def validate(self, potential, pos):
        good_vals = [str(x) for x in self.__values]
        result = QValidator.Invalid
        for v in good_vals:
            if v == potential:
                return (QValidator.Acceptable, pos)
            if v.startswith(potential):
                result = QValidator.Intermediate
            
        return (result, pos)
    

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
        
    


        