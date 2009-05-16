''' main.py
    Startup file that initializes the necessary objects and threads for the
    application
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

from atomicmetronome import AtomicMetronome as Metronome
from atomicparser import AtomicParser as Parser
from fsreceiver import FluidsynthReceiver as Receiver
import audiodriver
import conductor
import corecontroller
import gui
import score
import songinfo
import sys
    
# TEMP BETA: find soundfont source
import os.path
if sys.path[0] is not '':
	PATH = sys.path[0] + os.path.sep
else:
	PATH = ""

SOUNDFONT_FILE = PATH + 'HS_R8_Drums.sf2'

def init_core():
    pass
    
def init():
    song_info_object = songinfo.SongInfo()
    score_object = score.Score()
    conductor_object = conductor.Conductor(score_object, song_info_object)
    receiver_object = Receiver()
	# TEMP hardcoded for BETA
    receiver_object.soundfont_directory['metronome'] = SOUNDFONT_FILE
    receiver_object.soundfont_directory['handdrum'] = SOUNDFONT_FILE
	# TEMP BETA TEMP BETA
    parser_object = Parser(score_object, receiver_object)
    metronome_object = Metronome()
    metronome_object.addListener(conductor_object)
    metronome_object.addListener(parser_object)
    audio_driver_object = audiodriver.AudioDriver(metronome_object)
    audio_driver_object.start()
    core_controller_object = corecontroller.CoreController(audio_driver_object, \
            metronome_object, conductor_object, song_info_object)
    gui_object = gui.RRGuiMain([], core_controller_object)
    sys.exit(gui_object.run())
    print 'initializing gui modules'
    
if __name__ == '__main__':
	init()
	
        
