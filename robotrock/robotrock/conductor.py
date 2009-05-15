#!/usr/bin/env python
''' conductor.py
    Author: Alan Fineberg (af@cs.washington.edu)
    The conductor is responsible for telling the AI to perform,
    specifying their performance order, and keeping measure meta
    data up to date using its reference to song_info.
    The onPulse() method is triggered for each metronome pulse.
'''
import staff
import note

class Conductor(object):
    def __init__(self, score, song_info, staff_obj=staff.Staff, note_obj=note.Note):
        ''' 
        Create a conductor with a score, and a pointer to the current song
        information. The conductor is responsible for cueing each musician
        to play their respective measures, and must keep the measure
        meta data up to date for the musicians.
        The last two parameters are for testability purposes.
        '''
        self.score = score
        self.ensemble = []
        self.current_musician_measures = {}
        self.song_info = song_info
        self.measure_info = song_info.measureInfo()
        # Abstracting these constructor arguments aids testability.
        self.staff_obj = staff_obj
        self.note_obj = note_obj
        # Chunks allows us to keep our place within a measure.
        self.__chunks = 0
        self.chunks_per_beat = self.note_obj.note_values.QUARTER_NOTE
        self.__measures_played = 0
    
    def addMusician(self, musician):
        ''' Adds a musician and associates them with a staff, mapped one-to-one. '''
        self.ensemble.append(musician)
        self.__appendStaff(self.score, musician)
    
    def __appendStaff(self, score, musician):
        ''' When a musician is added to the score, it has its own staff to write to. '''
        score.staffs.append(self.staff_obj(instrument=musician.instrument))
        # Ensure that the musician starts playing at the correct measure.
        self.current_musician_measures[musician] = \
                score.staffs[-1].measures[self.__measures_played]
        
    def removeMusician(self, musician):
        ''' Prevents a musician from writing to the score. '''
        self.ensemble.remove(musician)
    
    def onPulse(self, duration):
        ''' 
        On every metronome tick, we check to see if we have reached the end of
        our current measure, and tell each musician to perform a measure
        with its metadata up to date.
        '''
        newMeasure = self.__chunks == 0

        # Update the measure info to reflect what's currently in song info.
        if newMeasure:
            self.measure_info = self.song_info.measureInfo()
            for musician in self.ensemble:
                self.__advanceMeasure(musician)
                self.__updateMeasureInfo(self.current_musician_measures[musician], \
                        self.measure_info)

        for (musician, measure) in self.current_musician_measures.iteritems():
            musician.compose(measure, self.__chunks, self.__chunks + duration)
    
        self.__updateLocation(duration)

    def __advanceMeasure(self, musician):
        ''' Internally changes the mapping of each musician to its current measure. '''
        measure = self.current_musician_measures[musician]
        self.current_musician_measures[musician] = measure.parent.measures.next()
        
    def __updateLocation(self, duration):
        ''' 
        Keep track of how far along we are in each measure. If we've reached
        the last beat, then reset __chunks so that the next pulse triggers
        the start of a new measure.
        '''
        beats_per_measure = self.measure_info['time_signature'][0]
        self.__chunks += duration
        
        if self.__chunks == self.chunks_per_beat * beats_per_measure:
            self.__chunks = 0
            self.__measures_played += 1

    def __updateMeasureInfo(self, measure, measure_info):
        ''' Uses measure_info to update measure meta data. '''
        measure.__dict__.update(measure_info)

if __name__ == '__main__':
    conductor = Conductor(['musician1', 'musician2'])