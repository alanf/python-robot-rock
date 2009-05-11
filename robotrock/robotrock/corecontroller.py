''' corecontroller.py
    Used by the GUI to interact with the audio portions of
    the application
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

import audiodriver
import conductor
import metronome
import musiciandirectory
import songinfo

MINIMUM_TEMPO = 0
MAXIMUM_TEMPO = 360


class CoreController():

    def __init__(self, audio_driver, metronome, conductor, songInfo):
        #Do initialization stuff
        self.metronome = metronome
        self.audio_driver = audio_driver
        self.conductor = conductor
        self.song_info = songInfo
        self.music_dir = musiciandirectory.MusicianDirectory()
    
    #Start the audio driver
    def play(self):
        self.audio_driver.play()
    
    #Pause the audio driver
    def pause(self):
        self.audio_driver.pause()
    
    # Halt the audio driver
    def halt(self):
        self.audio_driver.halt()
    
    # Sets the tempo of the metronome
    def setTempo(self, tempo):
        if tempo >= MINIMUM_TEMPO and tempo <= MAXIMUM_TEMPO:
            self.metronome.tempo = tempo
    
    # Update the time signature
    def updateTimeSignature(self, time_signature):
        if len(time_signature) == 2 and \
                time_signature[0] in songinfo.VALID_TIME_NUMERATOR and \
                time_signature[1] in songinfo.VALID_TIME_DENOMINATOR:
                    self.song_info.info['time_signature'] = time_signature
    
    # Update the key signature of the music
    def updateKeySignature(self, key_signature):
        if len(key_signature) == 3 and \
                key_signature[0] in songinfo.VALID_KEY and \
                key_signature[1] in songinfo.VALID_KEY_MODIFIERS and \
                key_signature[2] in songinfo.VALID_KEY_TONALITIES:
                    self.song_info.info['key_signature'] = key_signature
        
    # Adds the provided musician to the ensemble
    def addMusician(self, musician):
        self.conductor.addMusician(musician)
        
    # Removes the provided musician from the ensemble
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
        list = self.music_dir.validTags(tags)
        return list
    
  

