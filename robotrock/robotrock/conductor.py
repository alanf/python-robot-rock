#!/usr/bin/env python
''' conductor.py
    Author: Alan Fineberg (af@cs.washington.edu)
    The conductor is responsible for telling the AI to perform,
    and specifying their performance order.
    The onPulse() method is triggered for each metronome pulse.
'''
import staff

class Conductor(object):
    def __init__(self, score, songInfo):
        ''' 
        Create a conductor with a score, and a pointer to the current song
        information. The conductor is responsible for cueing each musician
        to play their respective measures, and must keep the measure
        meta data up to date for the musicians.
        '''
        self.score = score
        self.ensemble = []
        self.current_musician_measures = {}
        self.song_info = songInfo
        self.measure_info = songInfo.measureInfo()
        # Chunks allows us to keep our place within a measure.
        self.__chunks = 0
        # Fixme: These shouldn't be hardcoded. Load from a file.
        self.__chunk_values = {'tick': 1}
        self.chunks_per_beat = 192
    
    def addMusician(self, musician):
        ''' Adds a musician and associates them with a staff, mapped one-to-one. '''
        self.ensemble.append(musician)
        self.__appendStaff(self.score, musician)
    
    def __appendStaff(self, score, musician):
        score.staffs.append(staff.Staff(instrument=musician.instrument))
        # Assume no other entity adding or removing staffs (or single threaded).
        self.current_musician_measures[musician] = \
                self.__firstMeasureFromStaff(score.staffs[-1])
        
    def __firstMeasureFromStaff(self, staff):
        return staff.measures.next()
        
    def removeMusician(self, musician):
        self.ensemble.remove(musician)
    
    def onPulse(self, elapsed):
        ''' 
        On every metronome tick, we check to see if we have reached the end of
        our current measure, and tell each musician to performa a measure
        with its metadata up to date.
        '''
        newMeasure = self.__isNewMeasure(elapsed)
        
        # Update the measure info to reflect what's currently in song info.
        if newMeasure:
            self.measure_info = self.song_info.measureInfo()
            for musician in self.ensemble:
                self.__advanceMeasure(musician)

        for (musician, measure) in self.current_musician_measures.iteritems():
            musician.compose(measure, elapsed)
    
    def __isNewMeasure(self, elapsed):
        ''' 
        Keep track of how far along we are in each measure. If we've reached
        the last beat, then reset __chunks so that the next pulse triggers
        the start of a new measure.
        '''
        result = self.__chunks == 0
        
        # Returns the numerator of the time signature. Use our own 
        # internal copy of the measure_info, instead of what the user
        # might have modified.
        beatsInMeasure = self.measure_info['time_signature'][0]
        self.__chunks += self.__chunk_values[elapsed]
                
        if self.__chunks == self.chunks_per_beat * beatsInMeasure:
            self.__chunks = 0

        return result
        
    def __advanceMeasure(self, musician):
        measure = self.current_musician_measures[musician]
        self.current_musician_measures[musician] = measure.parent.measures.next()

    def __updateMeasureInfo(self, measure, measureInfo):
        measure.__dict__.update(measureInfo)

if __name__ == '__main__':
    conductor = Conductor(['musician1', 'musician2'])