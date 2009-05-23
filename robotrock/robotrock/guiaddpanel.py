"""
A widget that has controls for adding new musicians.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *


from walkingbassmusician import WalkingBass
from handdrum import HandDrum
#from musicians.handdrummusician import handdrum

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
    
    def addHandler(self, checked):
        if random.random() > 0.5:
            self.__guimain.stage.add_musician(WalkingBass())
        else:
            self.__guimain.stage.add_musician(HandDrum())
