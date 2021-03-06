"""
The main window for the RobotRock GUI.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""


from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from guistage import RRStage
from guiaddpanel import RRAddPanel
from guicontrolspanel import RRControlsPanel
from guimusicianinfopanel import RRMusicianInfoPanel

class RRMainWindow(QMainWindow):
    """
    The main window for the RobotRock GUI. Creates subcomponents
    RRStage, RRAddPanel, RRControlsPanel, and RRMusicianInfoPanel
    """
    def __init__(self, guimain, flags=Qt.WindowFlags()):
        """
        Creates a new mainwindow, given a reference to the guimain
        object and with the specified window flags.
        """
        super(RRMainWindow, self).__init__(None, flags)
        #self.setWindowState(Qt.WindowFullScreen)
        #self.setFocus()
        
        # The central widget is just a container for the grid below,
        #  it is nothing special.
        self.setCentralWidget(QWidget())
        
        #guimain.logger.debug("Creating RRMainWindow instance")
        
        self.__stage = RRStage(guimain)
        self.__addpanel = RRAddPanel(guimain)
        self.__controlspanel = RRControlsPanel(guimain)
        self.__musicianinfo = RRMusicianInfoPanel(guimain)
        
        # grid is set up in the following way:
        #       0   1
        #    0  a  mi
        #    1  s  mi
        #    2  s  cp
        # Where:
        #  a is the addpanel
        #  mi is the musician info panel
        #  cp is the controls panel
        #  s is the stage
        # cell (1,0) (the stage) has full stretch, others will stick to edges
        #
        # access cells via <row>, <col>
        
        grid = QGridLayout()
        
        grid.addWidget(self.__addpanel, 0, 0, Qt.AlignLeft | Qt.AlignTop)
        grid.addWidget(self.__stage, 1, 0, 2, 1)
        grid.addWidget(self.__musicianinfo, 0, 1, 2, 1, Qt.AlignRight | Qt.AlignTop)
        grid.addWidget(self.__controlspanel, 2, 1, Qt.AlignRight)
        
        # Make row 1 stretchy, column 0 stretchy
        grid.setRowStretch(1,1)
        grid.setColumnStretch(0,1)
        self.centralWidget().setLayout(grid)
    

