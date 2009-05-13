''' main.py
    Startup file that initializes the necessary objects and threads for the
    application
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

import audiodriver
import conductor
import corecontroller
import gui
import metronome
import score
import songinfo
import sys


def init_audio():
    print 'initializing audio'
    
def init_core():
    pass
    
def init_gui():
    print 'initializing gui modules'
    
if __name__ == '__main__':
        
        #init_core()
	songInfo = songinfo.SongInfo()
	score = score.Score()
	conductor = conductor.Conductor(score, songInfo)
	metronome = metronome.Metronome()
	audioDriver = audiodriver.AudioDriver(metronome)
	coreController = corecontroller.CoreController(audioDriver, metronome, conductor, songInfo)
	ui = gui.RRGuiMain([], coreController)
	sys.exit(ui.run())
	
        
