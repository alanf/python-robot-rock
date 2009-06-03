"""
A widget that has controls for adding new musicians.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *


import random
class RRAddPanel(QWidget):
    def __init__(self, guimain):
        super(RRAddPanel, self).__init__()
        #guimain.logger.debug("Creating add musician panel")
        
        self.__guimain = guimain
        self.__mlist = guimain.core.filterMusicianList([])
        
        if self.__mlist is None:
            # If we get here, then we're running under a fake CoreController.
            # Add the dummy musician so the GUI can still test things out.
            self.__mlist = []#[("dummy", lambda:MusicianDummy(guimain), "/Users/tjac0/Documents/UW/CSE/CSE 403/Robot_Rock/cse403/robotrock/images/old_metronome.png")]
        
        hpanel = QHBoxLayout()
        
        addbutton = QPushButton("Add musician")
        addbutton.setToolTip("Adds a musician to the stage")
        
        self.__mComboBox = QComboBox()
        self.__mComboBox.setToolTip("Selects a musician type")
        for musician in self.__mlist:
            self.__mComboBox.addItem(musician.name)
        
        self.connect(addbutton, SIGNAL('clicked(bool)'), self.addHandler)
        
        hpanel.addWidget(self.__mComboBox)
        hpanel.addWidget(addbutton)
        
        self.setLayout(hpanel)
    
    def addHandler(self, checked):        
        self.__guimain.stage.add_musician(self.__mlist[self.__mComboBox.currentIndex()])

class MusicianDummy(object):
    """
    Used in GUI debugging, this dummy class acts like a musician object
    to certain Gui classes (like MusicianWidget).
    """
    def __init__(self, guimain):
        self.__guimain = guimain
        self.instrument = "Dummy Musician"
    
    def setEnergy(self, val):
        #self.__guimain.logger.debug("Energy set to: %d" % val)
        pass
    
    def setComplexity(self, val):
        #self.__guimain.logger.debug("Complexity set to %d" % val)
        pass
    
    energy = property(fset=setEnergy)
    complexity = property(fset=setComplexity)
