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
        guimain.logger.debug("Fetching musician list")
        self.__mlist = guimain.core.filterMusicianList([])
        if self.__mlist is None:
            self.__mlist = [("dummy", MusicianDummy)]
        
        guimain.logger.debug("Musician list:")
        guimain.logger.debug(self.__mlist)
        
        hpanel = QHBoxLayout()
        
        addbutton = QPushButton("Add musician")
        addbutton.setToolTip("Adds a musician to the stage")
        
        self.__mComboBox = QComboBox()
        for musician in self.__mlist:
            self.__mComboBox.addItem(musician[0])
            guimain.logger.debug("Adding musician: %s" % musician[0])
        
        self.connect(addbutton, SIGNAL('clicked(bool)'), self.addHandler)
        
        hpanel.addWidget(self.__mComboBox)
        hpanel.addWidget(addbutton)
        
        self.setLayout(hpanel)
    
    def randomMusician(self):
        musicians = self.__guimain.core.filterMusicianList([])
        random_idx = int(random.random() * len(musicians))
        # Musicians are returned as a tuple of (name, constructor).
        return musicians[random_idx][1]()
        
    def addHandler(self, checked):
        self.__guimain.stage.add_musician(self.__mlist[self.__mComboBox.currentIndex()])

class MusicianDummy():
    def __init__(self):
        self.instrument = "Dummy Musician"
