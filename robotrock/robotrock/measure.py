#!/usr/bin/env python
''' measure.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Measure is a container for Notes, and also describes the current key and
    time signature, as well as other information necessary for playback of its
    notes.
'''
from expandinglist import ExpandingList
from note import Note

class Measure(object):
    def __init__(self, **measure_info):
        self.__dict__.update(measure_info)
        self.notes = []

    def addNote(self, Note):
        self.notes.append(Note)
    
    def orderedNotes(self):
        ''' Returns the notes in this measure ordered by start time.'''
        def compareNotes(a, b):
            ''' Returns the list of notes from earliest to latest.'''
            return a.start - b.start
        
        return sorted(self.notes, compareNotes)
    
    