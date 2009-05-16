#!/usr/bin/env python
# encoding: utf-8
"""
metronomemusician.py

Created by Alan Fineberg on 2009-05-03.
"""
import sys
import note
import dynamics
from drumkit import DrumKit

class MetronomeMusician(object):
    def __init__(self):
        self.instrument = 'metronome'
    
    def compose(self, measure, window_start, window_duration):
        if window_start == 0:
            print measure.time_signature[0]
            for i in range(0, measure.time_signature[0]):
                if i == 0:
                    my_tone = DrumKit["crash cymbal 1"]
                else:
                    my_tone=DrumKit["closed hi-hat"]
                myNote = note.Note(tone=my_tone, 
                        start=note.Note.note_values.QUARTER_NOTE * i, \
                        duration=note.Note.note_values.QUARTER_NOTE, \
                        rest=False, dynamic=dynamics.FORTE)
                measure.addNote(myNote)

