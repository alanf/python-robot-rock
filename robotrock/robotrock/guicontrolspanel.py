"""
This module is a set of controls for the RobotRock GUI.
It contains play/pause button, tempo slider, delete icon,
and a key selector.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from corecontroller import MAXIMUM_TEMPO, MINIMUM_TEMPO
from songinfo import VALID_KEY, VALID_KEY_TONALITIES, VALID_TIME_NUMERATOR, VALID_TIME_DENOMINATOR

class RRControlsPanel(QWidget):
    """
    A widget containing the play/pause button, tempo slider,
    trash icon, and key changer in a vertical layout.
    """
    def __init__(self, guimain):
        super(RRControlsPanel, self).__init__()
        #guimain.logger.debug("Creating controls widget")
        
        vpanel = QVBoxLayout()
        vpanel.addStretch(1)
        
        vpanel.addWidget(RRKeySelector(guimain), 0, Qt.AlignHCenter)
        vpanel.addWidget(RRTimeSelector(guimain), 0, Qt.AlignHCenter)
        
        vpanel.addWidget(RRTempoSlider(guimain), 0, Qt.AlignHCenter)
        vpanel.addWidget(RRPlayButton(guimain), 0, Qt.AlignHCenter)
        
        #vpanel.addWidget(RRDeleteIcon(guimain), 0, Qt.AlignHCenter)
        self.setLayout(vpanel)
        
    


class RRPlayButton(QPushButton):
    """
    A button allowing the user to either start or stop
    music generation.
    """
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
        """
        Called when the button is clicked. Toggles between play state
        and pause state.
        """
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
    """
    An icon assisting with the deletion of musician widgets.
    Clicking on this icon will delete the currently selected widget
    """
    def __init__(self, guimain):
        super(RRDeleteIcon, self).__init__("Delete Musician")
        #guimain.logger.debug("Creating delete icon")
        
        self.__guimain = guimain
        self.setToolTip("Delete the selected musician")
        
        self.setPixmap(guimain.getImage("delete-128x128.png").scaled(50,50,Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def mouseReleaseEvent(self, event):
        event.accept()
        if self.__guimain.focused_musician is not None:
            self.__guimain.focused_musician.close()


class RRTempoSlider(QWidget):
    """
    A slider widget allowing the user to set the song tempo.
    Contains a slider, a label, and a line box for direct
    setting of tempo.
    """
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
        
        self.connect(self.__slider, SIGNAL('sliderMoved(int)'), self.sliderHandler)
        self.connect(self.__slider, SIGNAL('sliderReleased()'), self.sliderHandler)
        self.connect(self.__value_label, SIGNAL('returnPressed()'), self.lineEditHandler)
        
        grid.addWidget(label, 0,0,Qt.AlignLeft | Qt.AlignBottom)
        grid.addWidget(self.__value_label, 0,1,Qt.AlignRight | Qt.AlignBottom)
        grid.addWidget(self.__slider,1,0,1,2)
        
        self.setLayout(grid)
        
        self.sliderHandler()
        
        self.setToolTip("Adjusts the tempo(speed) of the song")
    
    def sliderHandler(self):
        """
        Handler method is called whenever the slider value changes.
        Updates the CoreController and the lineEdit
        """
        val = self.__slider.value()
        self.__guimain.core.setTempo(val)
        self.__value_label.setText(str(val))
    
    def lineEditHandler(self):
        """
        Hander method is called whenever the user presses return
        after editing the lineEdit. Updates the CoreController and
        the slider.
        """
        val = int(self.__value_label.text())
        self.__guimain.core.setTempo(val)
        self.__slider.setValue(val)


class RRTimeSelector(QWidget):
    """
    This widget allows the user to select a time signature for the
    song. Currently only allows the beats per bar to change.
    """
    def __init__(self, guimain):
        super(RRTimeSelector, self).__init__()
        self.__guimain = guimain
        
        self.setToolTip("Selects how many quarter notes are in a single measure")
        
        grid = QGridLayout()
        
        self.__num = TimeSpinBox([x for x in VALID_TIME_NUMERATOR], guimain)
        self.__den = TimeSpinBox([x for x in VALID_TIME_DENOMINATOR], guimain)
        
        self.__time = (4,4)
        
        
        # Uncomment the two lines below to re-enable the denominator selector.
        #   This functionality is currently disabled, because it is not fully
        #   implemented in the musicians or the parser.
        grid.addWidget(QLabel("<b>Beats per bar: </b>"), 0,0,Qt.AlignVCenter | Qt.AlignRight)
        grid.addWidget(self.__num, 1,0,Qt.AlignHCenter)
        #grid.addWidget(self.__den, 1,1,Qt.AlignHCenter)
        
        self.connect(self.__num, SIGNAL('valueChanged(int)'), self.updateTime)
        #self.connect(self.__den, SIGNAL('valueChanged(int)'), self.updateTime)
        
        self.setLayout(grid)
    
    
    def updateTime(self, val):
        self.time = (self.__num.value(), self.__den.value())
    
    def settime(self, time):
        if self.__time != time:
            self.__guimain.core.updateTimeSignature(time)
            self.__time = time
        
    time = property(fset=settime)

class TimeSpinBox(QSpinBox):
    """
    A subclass of QSpinBox that selects its values from a list, and
    displays them in that order.
    """
    
    # On a side note, Qt makes implementing this particular behavior
    #  very difficult. I have no idea why, it seems a very useful feature.
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
        """
        Given a step value (such as 1 if the user pressed the up arrow, or -1
        if the user pressed the down arrow), adjusts the SpinBox to display the
        next value.
        Overrides QSpinBox.stepBy()
        """
        self.__index = self.__index + val
        self.setMinimum(self.__min)
        self.setMaximum(self.__max)
        if self.__index == 0:
            self.setMinimum(self.__values[self.__index])
        elif self.__index == len(self.__values) - 1:
            self.setMaximum(self.__values[self.__index])
        self.updateValue()
    
    def validate(self, potential, pos):
        """
        Checks to see if the current value in the box is valid.
        Returns a tuple of type (validity, cursor position)
        where validity is one of:
        QValidator.Acceptable   - The value is legal and valid
        QValidator.Intermediate - The value could be legal, if more was added
        QValidator.Invalid      - The value can never be valid
        """
        good_vals = [str(x) for x in self.__values]
        result = QValidator.Invalid
        for v in good_vals:
            if v == potential:
                return (QValidator.Acceptable, pos)
            if v.startswith(potential):
                result = QValidator.Intermediate
            
        return (result, pos)
    

class RRKeySelector(QWidget):
    """
    A widget allowing the user to select a musical key for the program.
    Allows a choice of [A,B,C,D,E,F,G], each with sharp and flat versions,
    as well as an option to make any key a minor key.
    """
    def __init__(self, guimain):
        super(RRKeySelector, self).__init__()
        self.__guimain = guimain
        
        self.setToolTip("Selects a key signature")
        
        self.__key = ('C', 'major')
        guimain.core.updateKeySignature(self.__key)
        
        # Converts 'b' to the unicode flat symbol,
        #  '#' to the unicode sharp symbol
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
        """
        Handles key changes originating from either the drop down list
        of keys or the checkbox for major/minor option.
        """
        if type(val) == type(0):
            # Change was from checkbox
            if val == 2:
                t = 'minor'
            else:
                t = 'major'
            self.__key = (self.__key[0], t)
        else:
            # Change was from drop down menu
            
            # Converts from unicode symbols back into 'b' and '#'
            k = val.replace(QChar(9837), 'b').replace(QChar(9839), '#')
            self.__key = (str(k), self.__key[1])
        
        self.__guimain.core.updateKeySignature(self.__key)
        
    


        