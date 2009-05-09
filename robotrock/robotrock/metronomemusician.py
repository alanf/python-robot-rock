#!/usr/bin/env python
# encoding: utf-8
"""
metronomemusician.py

Created by Alan Fineberg on 2009-05-03.
"""
import sys
import note

class MetronomeMusician(object):
    # HUGE PRECONDITION: The staff's measures list must have the
    # correct cursor location. In other words, the staff.measures.next()
    # is where we begin writing.
    def __init__(self):
        self.instrument = 'metronome'
        # FIXME: Make this able to handle other increment sizes.
        self.__duration_map = {'quarter': 1}
    
    def compose(self, measure, duration):
        myNote = note.Note(tone=42, duration='quarter', rest=False)
        measure.notes.append(myNote)