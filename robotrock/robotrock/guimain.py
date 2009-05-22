"""
Main entry point for the gui, as well as overall gui
coordinator. Includes references to logging facilities,
the core controller, and provides resource lookup.
Author: Tim Crossley <tjac0@cs.washington.edu>
"""


from PyQt4.QtCore import *
from PyQt4.QtGui  import *
import logging
import os
import sys

from guimainwindow import RRMainWindow

guimain = None

class RRGuiMain(object):
    def __init__(self, args=[], core=None):
        global guimain
        if guimain is not None:
            guimain.logger.critical("Attempted to create two objects of RRGuiMain!")
            raise RuntimeError, 'Attempted to create two objects of RRGuiMain!'
        
        guimain = self
        
        self.setup_logging()
        self.logger.debug("Initializing GUI...")
        
        if core is None:
            self.logger.warn("GUI created without core controller. Controller actions are disabled.")
            self.__core = CoreControllerDummy()
        else:
            self.__core = core
        
        ## Location sensing stuff
        directory, junk = os.path.split(os.path.abspath(sys.argv[0]))
        self.__parentdir, junk = os.path.split(directory)
        
        self.__stage = None
        
        self.__focusedmusician = None
        
        self.__infopanel = None
        self.__images = {}
        
        self.__app = QApplication(args)
        self.createNotFoundImage()
        
    
    def run(self):
        #self.logger.debug("Creating main window")
        self.__mainwindow = RRMainWindow(self)
        self.__mainwindow.show()
        self.logger.debug("Beginning Qt event loop")
        return self.__app.exec_()
    
    def setstage(self, stage):
        if self.__stage is not None:
            self.logger.error("Stage is being set multiple times!")
        else:
            #self.logger.debug("Setting stage object")
            pass
        self.__stage = stage
    
    def getstage(self):
        return self.__stage
    
    def setfocusedmusician(self, mwidget):
        if self.__focusedmusician is not mwidget:
            self.__focusedmusician = mwidget
            if self.__infopanel is not None:
                self.__infopanel.focusChanged(mwidget)
        
    
    def getfocusedmusician(self):
        return self.__focusedmusician
    
    def unfocusmusician(self, mwidget):
        if self.focused_musician is mwidget:
            self.focused_musician = None
    
    def getImage(self, image_name, scale=None, format=None):
        # Try cache first, then local, then global
        if self.__images.has_key(image_name):
            return self.__images[image_name][0]
        
        localname = os.path.join(self.__parentdir, 'images', image_name)
        if os.path.isfile(localname):
            self.logger.debug("Located image: %s" % localname)
            original = QPixmap(localname, format)
            if scale is not None:
                scaled = original.scaled(scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.__images[image_name] = (scaled, original)
            else:
                self.__images[image_name] = (original, original)
            return self.__images[image_name][0]
        
        globalname = os.path.join(sys.prefix, 'robotrockresources', 'images', image_name)
        if os.path.isfile(globalname):
            self.logger.debug("Located image: %s" % globalname)
            original = QPixmap(globalname, format)
            if scale is not None:
                scaled = image.scaled(scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.__images[image_name] = (scaled, original)
            else:
                self.__images[image_name] = (original, original)
            return self.__images[image_name][0]
        
        self.logger.error("Failed to find image: %s" % image_name)
        return QPixmap(self.__notfoundimage)
    
    def updateImageSize(self, image_name, scale):
        if not self.__images.has_key(image_name):
            self.logger.warn("Calling update image size on an image not yet loaded..")
            self.getImage(image_name, scale)
            return
        
        scaled, original = self.__images[image_name]
        if not scaled.size() == scale:
            self.__images[image_name] = (original.scaled(scale, Qt.KeepAspectRatio, Qt.SmoothTransformation), original)
    
    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG)
        self.__logger = logging.getLogger('robotrock.gui')
    
    def createNotFoundImage(self):
        self.__notfoundimage = QPixmap(128,128)
        painter = QPainter(self.__notfoundimage)
        adjusted_rect = self.__notfoundimage.rect().adjusted(0,0,-1,-1)
        painter.drawRect(adjusted_rect)
        painter.drawLine(adjusted_rect.topLeft(), adjusted_rect.bottomRight())
        painter.drawLine(adjusted_rect.topRight(), adjusted_rect.bottomLeft())
        painter.setPen(Qt.red)
        painter.setBackgroundMode(Qt.OpaqueMode)
        painter.drawText(adjusted_rect, Qt.AlignCenter, "Image Not Found!")
        del painter
    
    def getlogger(self):
        return self.__logger
    
    def getcore(self):
        return self.__core
    
    def setInfoPanel(self, infopanel):
        if self.__infopanel is not None:
            self.logger.error("Attempt to attach multiple info panels!")
        self.__infopanel = infopanel
    
    logger           = property(getlogger)
    core             = property(getcore)
    stage            = property(getstage, setstage)
    focused_musician = property(getfocusedmusician, setfocusedmusician)
    


from corecontroller import CoreController
import functools
class CoreControllerDummy():
    def __init__(self):
        def logfunction(name, *args):
            global guimain
            guimain.logger.info("Called %s with args: %s" % (name, str(args)))
        
        # print CoreController.__dict__
        for key in CoreController.__dict__:
            value = CoreController.__dict__[key]
            if type(value) == type(lambda:0) and key is not "__init__":
                self.__dict__[key] = functools.partial(logfunction, key)
            
        
    

if __name__ == '__main__':
    guiobject = RRGuiMain()
    sys.exit(guiobject.run())