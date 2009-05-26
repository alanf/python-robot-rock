''' corecontroller.py
    Used by the GUI to interact with the audio portions of
    the application
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

import audiodriver
import conductor
import musiciandirectory
import songinfo

MINIMUM_TEMPO = 40
MAXIMUM_TEMPO = 208


class CoreController():


    def __init__(self, audio_driver, metronome, conductor, songInfo, \
        musician_directory):
        #Do initialization stuff
        self.metronome = metronome
        self.audio_driver = audio_driver
        self.conductor = conductor
        self.song_info = songInfo
        self.music_dir = musician_directory
    
    #Start the audio driver
    def play(self):
	#print 'playing'
        self.audio_driver.play()
    
    #Pause the audio driver
    def pause(self):
	#print 'paused'
        self.audio_driver.pause()
    
    # Halt the audio driver
    def halt(self):
        self.audio_driver.halt()
    
    # Sets the tempo of the metronome (clamped to the min/max values)
    # Param: tempo, an integer
    def setTempo(self, tempo):
        tempo = min(MAXIMUM_TEMPO, tempo)
	tempo = max(MINIMUM_TEMPO, tempo)
        self.metronome.tempo = tempo
    
    # Update the time signature
    # Param: time_signature, a 2-tuple of a numerator and denominator
    def updateTimeSignature(self, time_signature):
        if len(time_signature) == 2 and \
	        time_signature[0] in songinfo.VALID_TIME_NUMERATOR and \
                time_signature[1] in songinfo.VALID_TIME_DENOMINATOR:
                    self.song_info.info['time_signature'] = time_signature
    
    # Update the key signature of the music
    # Param: key_signature, a 2-tuple of key, and tonality
    #        See songinfo.py for legal values of the tuple's elements
    def updateKeySignature(self, key_signature):
        if len(key_signature) == 2 and \
	        key_signature[0] in songinfo.VALID_KEY and \
                key_signature[1] in songinfo.VALID_KEY_TONALITIES:
                    self.song_info.info['key_signature'] = key_signature
    
    # Adds the provided musician to the ensemble
    # Param: musician, the musician to be added
    def addMusician(self, musician):
        self.conductor.addMusician(musician)
        
    # Removes the provided musician from the ensemble, if musician is
    # present in ensemble
    # Param: musician, the musician to be removed
    def removeMusician(self, musician):
        if musician in self.conductor.ensemble:
            self.conductor.removeMusician(musician)
        
    # Returns a list of musicians that satisfy the provided tags
    def filterMusicianList(self, tags):
        tag_set = set()
        for tag in tags:
            tag_set.add(tag)
        list = self.music_dir.filterMusicianList(tag_set)
        return list
    
    # Returns a list of tags whose intersection with the provided tags
    # is not the empty set.
    def validTags(self, tags):
        tag_set = set()
        for tag in tags:
            tag_set.add(tag)
        list = self.music_dir.validTags(tag_set)
        return list
    
  

