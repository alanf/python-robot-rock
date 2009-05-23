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
import guimain
import musiciandirectory
import realtimeclock
import score
import songinfo
import sys
    
# TEMP BETA: find soundfont source
import os.path
if sys.path[0] is not '':
    PATH = sys.path[0] + os.path.sep
else:
    PATH = ""

#SOUNDFONT_FILE = sys.prefix + '/robotrockresources/sounds/' + 'HS_R8_Drums.sf2'
SOUNDFONT_FILE = '../soundfonts/HS_R8_Drums.sf2'
BASS_FILE = '../soundfonts/JazzAcousticBass.sf2'

def init_core():
    pass
    
def init():
    song_info_object = songinfo.SongInfo()
    score_object = score.Score()
    conductor_object = conductor.Conductor(score_object, song_info_object)
    soundfont_directory = { # New hardcoded format. ;) Will be fixed TONIGHT! - Travis
        'metronome' : (SOUNDFONT_FILE, 0, 0),
        'handdrum'  : (SOUNDFONT_FILE, 0, 0),
        'jazz bass' : (BASS_FILE, 0, 1)
    }
    receiver_object = Receiver( soundfont_directory )
    parser_object = Parser(score_object, receiver_object)
    clock_object = realtimeclock.RealtimeClock()
    metronome_object = Metronome()
    metronome_object.addListener(conductor_object)
    metronome_object.addListener(parser_object)
    audio_driver_object = audiodriver.AudioDriver(clock_object, metronome_object)
    audio_driver_object.start()
    musician_directory_object = musiciandirectory.MusicianDirectory()
    core_controller_object = corecontroller.CoreController(audio_driver_object, \
        metronome_object, conductor_object, song_info_object, \
	musician_directory_object)
    gui_object = guimain.RRGuiMain([], core_controller_object)
    sys.exit(gui_object.run())
    print 'initializing gui modules'
    
if __name__ == '__main__':
    init()
    
        
