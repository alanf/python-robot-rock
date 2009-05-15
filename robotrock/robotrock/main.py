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


def init_audio():
    print 'initializing audio'
    
def init_core():
    pass
    
def init_gui():
    song_info_object = songinfo.SongInfo()
    score_object = score.Score()
    conductor_object = conductor.Conductor(score_object, song_info_object)
    receiver_object = Receiver()
    receiver_object.soundfont_directory['metronome'] = 'HS_R8_Drums.sf2' # TEMP hardcoded for BETA
    receiver_object.soundfont_directory['handdrum'] = 'HS_R8_Drums.sf2'
#   parser_object = Parser(score_object, receiver_object)
    metronome_object = Metronome()
    metronome_object.addListener(conductor_object)
#   metronome_object.addListener(parser_object)
    audio_driver_object = audiodriver.AudioDriver(metronome_object)
    audio_driver_object.start()
    core_controller_object = corecontroller.CoreController(audio_driver_object, metronome_object, conductor_object, song_info_object)
    gui_object = gui.RRGuiMain([], core_controller_object)
    sys.exit(gui_object.run())
    print 'initializing gui modules'
    
if __name__ == '__main__':
        
        #init_core()
	init_gui()
	
        
