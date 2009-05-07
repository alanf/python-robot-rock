''' metronome.py
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

from audiodriver import AudioDriver
from conductor import Conductor
from metronome import Metronome
from musiciandirectory import MusicianDirectory


class CoreController():
    def __init__(self):
        #Do initialization stuff
        self.conductor = Conductor([])
        self.metronome = Metronome()
        self.music_dir = MusicianDirectory()
        self.audio_driver = AudioDriver(self.metronome)    

    def play(self):
        #Start the play sequence  
        print 'playing metronome'
        self.audio_driver.play()
      
    def pause(self):
        #Pause the metronome
        print 'pausing metronome'
        self.audio_driver.pause()
	
    def halt(self):
        #Halt the metronome
        print 'halting metronome'
        self.audio_driver.halt()    
	
    def setTempo(self, tempo):
        print 'setting metronome tempo'
        self.metronome.setTempo(tempo)

    def updateSongInfo(self, key_signature, time_signature):
        #Update the key and time signatures
        print 'updating song info'

    def addMusician(self, musician):
        print 'calling Conductor to add musician'
        self.conductor.addMusician(musician)
        
    def removeMusician(self, musician):
        print 'calling Conductor to remove musician'
        self.conductor.removeMusician(musician)
        
    def filterMusicianList(self, tags):
        print 'calling MusicianDirectory to filter musician list'
        tag_set = set()
        for tag in tags:
            tag_set.add(tag)
        list = self.music_dir.filterMusicianList(tag_set)
        return list
        
        
  

