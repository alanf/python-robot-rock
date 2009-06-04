"""
This component displays information about the currently
selected musician widget.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import functools

class RRMusicianInfoPanel(QWidget):
    """
    This widget displays information about the currently
    selected musician widget.
    """
    def __init__(self, guimain):
        """
        Creates a new info panel, given a reference to the
        guimain object.
        """
        super(RRMusicianInfoPanel, self).__init__()
        self.__guimain = guimain
        
        self.setToolTip("Displays information and properties about musicians on the stage")
        
        stacked = QStackedLayout()
        self.__mwidget_detail = RRMWidgetDetail(guimain)
        
        self.__none_detail = QLabel("No musician\nselected")
        self.__none_detail.setAlignment(Qt.AlignCenter)
        
        stacked.addWidget(self.__none_detail)
        stacked.addWidget(self.__mwidget_detail)
        stacked.setCurrentIndex(0)        
        
        self.setLayout(stacked)
        guimain.setInfoPanel(self)
    
    def focusChanged(self, mwidget):
        """
        Called by the guimain whenever the focused musician widget
        changes. If mwidget is None, the info panel displays its
        default 'no musician selected' message.
        """
        if mwidget is not None:
            self.__mwidget_detail.setMWidget(mwidget)
            self.layout().setCurrentIndex(1)
        else:
            self.layout().setCurrentIndex(0)
        



class RRMWidgetDetail(QGroupBox):
    """
    This widget directly displays information about a musician
    widget. It is used as a subcomponent of RRMusicianInfoPanel.
    """
    def __init__(self, guimain):
        super(RRMWidgetDetail, self).__init__("Musician Detail")
        
        self.__guimain = guimain
        
        grid = QGridLayout()
        #grid.addWidget(QLabel("<b><i>Musician Detail </i></b>"),0,0,1,2, Qt.AlignHCenter|Qt.AlignTop)
        grid.addWidget(QLabel("Energy: "),0,0,Qt.AlignRight)
        grid.addWidget(QLabel("Complexity: "),1,0,Qt.AlignRight)
        
        self.__energyField = QLabel()
        self.__energyField.setMaximumWidth(50)
        grid.addWidget(self.__energyField, 0,1,Qt.AlignLeft)
        
        self.__complexityField = QLabel()
        self.__complexityField.setMaximumWidth(50)
        grid.addWidget(self.__complexityField, 1,1,Qt.AlignLeft)
        
        self.__deleteButton = QPushButton("Delete Musician")
        self.__deleteButton.setToolTip("Deletes the currently selected musician")
        #self.__deleteButton.setIconSize(QSize(50,50))
        #self.__deleteButton.setIcon(QIcon(guimain.getImage("delete-128x128.png", QSize(50,50))))
        grid.addWidget(self.__deleteButton, 2,0,1,2,Qt.AlignHCenter | Qt.AlignTop)
        
        self.__mwidget = None
        
        self.__del_set = set([])
        
        self.setLayout(grid)
    
    def setEnergy(self, val):
        self.__energyField.setText(str(val))
    
    def setComplexity(self, val):
        self.__complexityField.setText(str(val))
    
    def setMWidget(self, mwidget):
        self.__mwidget = mwidget
        self.setTitle("%s detail" % mwidget.getImageName())
        self.setEnergy(mwidget.energy)
        self.setComplexity(mwidget.complexity)
        self.connect(mwidget, SIGNAL("energyChanged"), self.setEnergy)
        self.connect(mwidget, SIGNAL("complexityChanged"), self.setComplexity)
        self.connect(self.__deleteButton, SIGNAL("clicked(bool)"), self.deleteButton)
    
    def deleteButton(self, ignore):
        if self.__mwidget is not None and self.__mwidget.num not in self.__del_set:
            self.__del_set.add(self.__mwidget.num)
            self.__guimain.logger.debug("Delete button clicked for musician: %d" % self.__mwidget.num)
            self.__mwidget.close()
        
    

