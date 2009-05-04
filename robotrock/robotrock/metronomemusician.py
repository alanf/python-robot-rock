#!/usr/bin/env python
# encoding: utf-8
"""
metronomemusician.py

Created by Alan Fineberg on 2009-05-03.
"""
import sys
from note import Note

class MetronomeMusician(object):
    # HUGE PRECONDITION: The staff's measures list must have the
    # correct cursor location. In other words, the staff.measures.next()
    # is where we begin writing.
    def __init__(self, staff):
        self.staff = staff
        self.__steps = 0
        self.instrument = 'metronome'
        # FIXME: Make this able to handle other increment sizes.
        self.__duration_map = {'quarter': 1}
    
    def play(self, duration):
        if self.__steps == 0:
            print 'next measure: musician'
            # We're at the start of a new measure.
            self.current_measure = self.staff.measures.next()

            # Get the key signature, but don't do anything with it.
            self.key =  self.current_measure.key
            self.time_signature =  self.current_measure.time_signature
            # Special beat just on the first tick of a measure.
            note = Note(tone=38, duration='quarter', rest=False)
        
        else:
            # Add one quarter note.
            note = Note(tone=42, duration='quarter', rest=False)
        
        self.current_measure.notes.append(note)
        
        # Keep our place in the current measure.
        self.__steps += self.__duration_map[duration]
        
        # FIXME: Make time signature a named dictionary, instead of a tuple
        # such as (4, 4).
        if self.time_signature[0] == self.__steps:
            self.__steps = 0
