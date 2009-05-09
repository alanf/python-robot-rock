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
from note import Note

class SimpleParser(object):
    def __init__(self, score, synth):
        self.synth = synth
        self.score = score
        self.total_duration = 0
        self.duration_dict = {'tick': 1, 'quarter': 1} #'quarter': 16, 'thirty-second': 2}
        self.measures_played = -1
        
    def onPulse(self, duration):     
        if self.total_duration % 4 == 0:
            self.measures_played += 1
            self.current_slice = self.score.score_slices.next()

        # Reinspects the measure to see if a musician added more notes.
        if True:
            self.notes = ExpandingList(object=list)
             
            for measure in self.current_slice:
                segment = 0
                for (i, note) in enumerate(measure.notes):
                    self.notes[i].append(note.tone)             
                    segment += self.duration_dict[note.duration]
            
        i = self.total_duration % 4
        self.total_duration += self.duration_dict[duration]
        self.__play(i)
              
    def __play(self, index):
        for note in self.notes[index]:
            self.noteOn(note)

    def noteOn(self, note):
        self.synth.noteon(0, note, 127)
