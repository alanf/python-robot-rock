#!/usr/bin/env python
# encoding: utf-8
"""
activemusician.py

Created by Alan Fineberg on 2009-05-03.
"""
import sys
import note
import dynamics
import drumkit

class ActiveMusician(object):
    def __init__(self):
        self.instrument = 'metronome'
        self._energy = 50
        self._complexity = 50
        self.changed = False
    
    def compose(self, measure, window_start, window_duration):
        if window_start == 0 or self.changed:
            if self.changed:
                measure.notes = []
                self.changed = False
                
            my_duration = note.Note.note_values.QUARTER_NOTE
            
            if self._energy > 60:
                my_duration = my_duration // 4
            elif self._energy > 50:
                my_duration = my_duration // 2
            elif self._energy < 25:
                    my_duration = my_duration * 2 // 1
        
            my_start = 0
        
            if self._complexity > 50:
                note.Note.note_values.EIGHTH_NOTE_TRIPLET
                my_duration = my_duration * 3 // 2
            elif self._complexity > 30:
                start = note.Note.note_values.EIGHTH_NOTE
                my_duration = my_duration * 3 // 2
        
            total_duration = my_start
            i = 0
            while total_duration < note.Note.note_values.QUARTER_NOTE * 4:
                myNote = note.Note(tone=drumkit.DrumKit['open hi-hat'], \
                        start=my_start +i*my_duration, \
                        duration=my_duration, \
                        rest=False, dynamic=dynamics.FORTE)
                measure.addNote(myNote)
                total_duration += my_duration
                i += 1

    def __setComplexity(self, value):
        self._complexity = value
        self.changed = True
    
    def __setEnergy(self, value):
        self._energy = value
        self.changed = True
    
    complexity = property(fset=__setComplexity)
    energy = property(fset=__setEnergy)

