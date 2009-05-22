"""
A widget that has controls for adding new musicians.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from activemusician import ActiveMusician

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
        self.__guimain.stage.add_musician(ActiveMusician())
