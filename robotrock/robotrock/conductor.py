#!/usr/bin/env python
''' conductor.py
    Author: Alan Fineberg (af@cs.washington.edu)
    The conductor is responsible for telling the AI to perform,
    specifying their performance order, and keeping measure meta
    data up to date using its reference to song_info.
    The onPulse() method is triggered for each metronome pulse.
'''
import copy
import staff
import note
import conductorscoremarker

class Conductor(object):
    def __init__(self, score, song_info, note_obj=note.Note):
        ''' 
        Create a conductor with a score, and a pointer to the current song
        information. The conductor is responsible for cueing each musician
        to play their respective measures, and must keep the measure
        meta data up to date for the musicians.
        The last two parameters are for testability purposes.
        '''
        self.score_marker = conductorscoremarker.ConductorScoreMarker(score)
        self.ensemble = []
        self.musician_staffs = {}
        self.song_info = song_info
        # Abstracting this constructor arguments aids testability.
        self.note_obj = note_obj
        self.new_musicians = False
    
    def addMusician(self, musician):
        ''' Adds a musician and associates them with a staff, mapped one-to-one. '''
        self.ensemble.append(musician)
        self.musician_staffs[musician] = self.score_marker.addStaff(musician.instrument)
        self.new_musicians = True
                        
    def removeMusician(self, musician):
        ''' Prevents a musician from writing to the score. '''
        self.ensemble.remove(musician)
    
    def onPulse(self, duration):
        ''' 
        On every metronome tick, we check to see if we have reached the end of
        our current measure, and tell each musician to perform a measure
        with its metadata up to date.
        '''
        staff_measures = self.score_marker.staffMeasures()
        measure_position = self.score_marker.measure_position
        
        # Perform the book keeping of getting the latest measure info.
        if measure_position == 0:
            self.measure_info = self.song_info.measureInfo()
        if measure_position == 0 or self.new_musicians:
            for (staff, measure) in staff_measures.iteritems():
                self.__updateMeasureInfo(measure, self.measure_info)
                
        # Using a mapping of musician -> staff, staff -> measure,
        # have each musician compose their respective measure.      
        for (musician, staff) in self.musician_staffs.iteritems():
            if staff in staff_measures.keys() and musician in self.ensemble:
                musician.compose(staff_measures[staff], \
                        measure_position, \
                        measure_position + duration,
                        copy.copy(self.score_marker.score_slices))
        
        self.score_marker.forward(duration)
        
    def __updateMeasureInfo(self, measure, measure_info):
        ''' Uses measure_info to update measure meta data. '''
        measure.__dict__.update(measure_info)
