''' main.py
    Startup file that initializes the necessary objects and threads for the
    application
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

import audiodriver
import conductor
import corecontroller
import metronome
import score
import songinfo


def init_audio():
    print 'initializing audio'
    
def init_core():
    
    
def init_gui():
    print 'initializing gui modules'
    
if __name__ == '__main__':
        
        #init_core()
	songInfo = songinfo.SongInfo()
	score = score.Score()
	conductor = conductor.Conductor(score, songInfo)
	metronome = metronome.Metronome()
	audioDriver = audiodrvier.AudioDriver()
	coreController = corecontroller.CoreController(audioDriver, metronome, conductor, songInfo)
	
        
