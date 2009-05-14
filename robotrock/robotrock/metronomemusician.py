#!/usr/bin/env python
# encoding: utf-8
"""
metronomemusician.py

Created by Alan Fineberg on 2009-05-03.
"""
import sys
import note
import dynamics

class MetronomeMusician(object):
    def __init__(self):
        self.instrument = 'metronome'
    
    def compose(self, measure, window_start, window_duration):
        print window_start
        myNote = note.Note(tone=42, start=window_start, \
                duration=note.Note.note_values.QUARTER_NOTE, \
                rest=False, dynamic=dynamics.FORTE)
        measure.addNote(myNote)