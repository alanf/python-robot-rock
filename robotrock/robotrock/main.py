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
import soundfontdirectory
    
# TEMP BETA: find soundfont source
import os.path
if sys.path[0] is not '':
    PATH = sys.path[0] + os.path.sep
else:
    PATH = ""

SOUNDFONT_DIRECTORY_FILE = sys.prefix + '/robotrockresources/' + 'soundfonts/basic_set.txt'

def init_core():
    pass
    
def init():
    song_info_object = songinfo.SongInfo()
    score_object = score.Score()
    conductor_object = conductor.Conductor(score_object, song_info_object)
    soundfont_directory = soundfontdirectory.load( SOUNDFONT_DIRECTORY_FILE )
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
    
        
