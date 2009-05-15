#!/usr/bin/env python
# encoding: utf-8
"""
activemusician.py

Created by Alan Fineberg on 2009-05-03.
"""
import sys
import note
import dynamics

class ActiveMusician(object):
    def __init__(self):
        self.instrument = 'metronome'
        self.energy = 50
        self.complexity = 50
    
    def compose(self, measure, window_start, window_duration):
        if window_start == 0:
            my_duration = note.Note.note_values.QUARTER_NOTE
            if self.energy > 75:
                duration *= 2
                duration = duration // 1
            elif self.energy < 25:
                duration = duration // 2
        
            my_start = 0
            if self.complexity > 50:
                start = note.Note.note_values.EIGHTH_NOTE
            if self.complexity > 75:
                note.Note.note_values.EIGHTH_NOTE_TRIPLET
        
            total_duration = my_start
            while total_duration < note.Note.note_values.QUARTER_NOTE * 4:
                myNote = note.Note(tone=42, start=my_start, \
                        duration=my_duration, \
                        rest=False, dynamic=dynamics.FORTE)
                measure.addNote(myNote)
                total_duration += my_duration

if __name__ == '__main__':
    m = MetronomeMusician()
