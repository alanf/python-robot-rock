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
        
        hpanel = QHBoxLayout()
        
        addbutton = QPushButton("Add musician")
        addbutton.setToolTip("Adds a musician to the stage")
        self.connect(addbutton, SIGNAL('clicked(bool)'), self.addHandler)
        
        hpanel.addWidget(addbutton)
        
        self.setLayout(hpanel)
    
    def randomMusician(self):
        musicians = self.__guimain.core.filterMusicianList([])
        random_idx = int(random.random() * len(musicians))
        # Musicians are returned as a tuple of (name, constructor).
        return musicians[random_idx][1]()
        
    def addHandler(self, checked):
        if dir(self.__guimain.core).__contains__("dummy"):
            self.__guimain.stage.add_musician(MusicianDummy())
        else:
            self.__guimain.stage.add_musician(self.randomMusician())

class MusicianDummy():
    def __init__(self):
        self.instrument = "Dummy Musician"
