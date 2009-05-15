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
	print 'energy', self.energy, 'complex', self.complexity
        if window_start == 0:
            my_duration = note.Note.note_values.QUARTER_NOTE
            if self.energy > 75:
                my_duration = my_duration // 4
	    elif self.energy > 60:
		my_duration = my_duration // 2
            elif self.energy < 25:
                my_duration = my_duration * 2 // 1
        
            my_start = 0
            if self.complexity > 30:
                start = note.Note.note_values.EIGHTH_NOTE
		my_duration = my_duration * 3 // 2
            if self.complexity > 60:
                note.Note.note_values.EIGHTH_NOTE_TRIPLET
		my_duration = my_duration * 3 // 2
        
            total_duration = my_start
	    i = 0
            while total_duration < note.Note.note_values.QUARTER_NOTE * 4:
                myNote = note.Note(tone=42, start=my_start +i*my_duration, \
                        duration=my_duration, \
                        rest=False, dynamic=dynamics.FORTE)
                measure.addNote(myNote)
                total_duration += my_duration
		i += 1

if __name__ == '__main__':
    m = MetronomeMusician()
