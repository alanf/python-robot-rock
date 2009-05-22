"""
The stage on which the musicians are added, moved around, and deleted.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import functools

class RRMusicianInfoPanel(QWidget):
    def __init__(self, guimain):
        super(RRMusicianInfoPanel, self).__init__()
        #guimain.logger.debug("Creating musician info panel")
        
        self.__guimain = guimain
        
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
        if mwidget is not None:
            self.__mwidget_detail.setEnergy(mwidget.energy)
            self.__mwidget_detail.setComplexity(mwidget.complexity)
            self.connect(mwidget, SIGNAL("energyChanged"), self.__mwidget_detail.setEnergy)
            self.connect(mwidget, SIGNAL("complexityChanged"), self.__mwidget_detail.setComplexity)
            self.layout().setCurrentIndex(1)
        else:
            self.layout().setCurrentIndex(0)
        



class RRMWidgetDetail(QWidget):
    def __init__(self, guimain):
        super(RRMWidgetDetail, self).__init__()
        
        grid = QGridLayout()
        grid.addWidget(QLabel("<b><i>Musician Detail </i></b>"),0,0,1,2, Qt.AlignHCenter|Qt.AlignTop)
        grid.addWidget(QLabel("Energy: "),1,0,Qt.AlignRight)
        grid.addWidget(QLabel("Complexity: "),2,0,Qt.AlignRight)
        
        self.__energyField = QLineEdit()
        self.__energyField.setReadOnly(True)
        self.__energyField.setFocusPolicy(Qt.NoFocus)
        self.__energyField.setMaximumWidth(50)
        grid.addWidget(self.__energyField, 1,1,Qt.AlignLeft)
        
        self.__complexityField = QLineEdit()
        self.__complexityField.setReadOnly(True)
        self.__complexityField.setFocusPolicy(Qt.NoFocus)
        self.__complexityField.setMaximumWidth(50)
        grid.addWidget(self.__complexityField, 2,1,Qt.AlignLeft)
        
        self.setLayout(grid)
    
    def setEnergy(self, val):
        self.__energyField.setText(str(val))
    
    def setComplexity(self, val):
        self.__complexityField.setText(str(val))

