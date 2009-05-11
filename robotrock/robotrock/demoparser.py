#!/usr/bin/env python
# encoding: utf-8
"""
demoparser.py

Created by Alan Fineberg on 2009-05-02.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from expandinglist import ExpandingList
import note

class SimpleParser(object):
    def __init__(self, score, synth):
        self.synth = synth
        self.score = score
        self.total_duration = 0
        self.durations = note.Note.note_values
        self.measures_played = -1
        
    def onPulse(self, duration):     
        # Assumes 4 / 4 measures.
        if self.total_duration % self.durations.WHOLE_NOTE == 0:
            self.measures_played += 1
            self.current_slice = self.score.score_slices.next()

        # Reinspects the measure to see if a musician added more notes.
        if True:
            self.notes = ExpandingList(object=list)
             
            for measure in self.current_slice:
                for note in measure.orderedNotes():
                    self.notes[note.start].append(note)             
        
        i = self.total_duration % self.durations.WHOLE_NOTE
                
        self.total_duration += duration
        self.__play(i)
              
    def __play(self, index):
        for note in self.notes[index]:
            if not note.rest:
                print 'note on'
                self.noteOn(note)

    def noteOn(self, note):
        self.synth.noteon(0, note.tone, 127)
