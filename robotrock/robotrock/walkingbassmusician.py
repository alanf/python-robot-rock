#!/usr/bin/env python
# encoding: utf-8
"""
walkingbassmusician.py

Created by Alan Fineberg on 2009-05-21.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import activemusician
import note
import tone
import dynamics
import random


class WalkingBass(activemusician.ActiveMusician):
    def __init__(self):
        activemusician.ActiveMusician.__init__(self)
        self.instrument = 'jazz bass'
    
    def compose(self, measure, window_start, window_duration):
        if window_start == 0 or self.changed:
            if self.changed:
                measure.notes = []
                self.changed = False
        
            complexity = self._complexity / 100.0
            beat_value = note.Note.note_values.HALF_NOTE
            if self._energy > 50:
                beat_value = note.Note.note_values.EIGHTH_NOTE
            if self._energy > 75:
                beat_value = note.Note.note_values.SIXTEENTH_NOTE
                
            notes = self.createSyncopatedRhythm(measure.time_signature[0], \
                    beat_value, \
                    complexity)
            
            # The root note is specified by the key signature, and the third piano octave.
            root = (measure.key_signature[0], 3)
            minor = measure.key_signature[1] == 'minor'
            for my_note in notes:
                my_note.dynamic = dynamics.FORTE 
                my_note.tone = self.chooseTone(root, complexity, minor)
  
        
            for my_note in notes:
                my_note.dynamic = dynamics.FORTE
                measure.addNote(my_note)

    def chooseTone(self, root, complexity, minor=False):
        # Root note.
        if random.random() > complexity:
            return root
        # The third note.
        elif random.random() > complexity / 2:
            if not minor:
                return (tone.getTone(root, tone.MEDIANT))
            else:
                return (tone.getTone(root, tone.MINOR_MEDIANT))
          # The fifth note.
        elif random.random() > complexity / 3:
            return (tone.getTone(root, tone.DOMINANT))
        # The forth note.
        elif random.random() > complexity / 4:
            return (tone.getTone(root, tone.SUBDOMINANT))
        # The sixth or minor seventh note.
        else:
            if not minor:
                return (tone.getTone(root, tone.SUBMEDIANT))
            else:
                return (tone.getTone(root, tone.SUBTONIC))
        
    def createSyncopatedRhythm(self, beats, base_rhythm, syncopation):
        notes = []
        beat_number = 0
        current_start = 0
        
        while current_start <= note.Note.note_values.QUARTER_NOTE * beats:
            my_note = note.Note(duration=base_rhythm)
            # Adjusts the liklihood of a note based on whether it's an on or off beat.
            if random.random() * 2.0 > abs((1 * (beat_number % 2)) - syncopation):
                my_note.start = current_start
                notes.append(my_note)
            current_start += base_rhythm
            beat_number += 1
            
        return notes
                    
if __name__ == '__main__':
    wbm = WalkingBassMusician()
        

