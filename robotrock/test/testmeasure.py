#!/usr/bin/env python
# encoding: utf-8
''' testmeasure.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Unit Tests for Measure.
'''

import sys
import unittest

class TestMeasure(unittest.TestCase):
    def setUp(self):
        pass
    
    def testCreateMeasure(self):
        measure = Measure(key=('C', '#', 'maj'), time=(4, 4), tempo=(120, 'bpm'))
        # Compare tuples using string comparison.
        self.assertEquals(str(measure.key), str(('C', '#', 'maj')))
        self.assertEquals(str(measure.tempo), str((120, 'bpm')))
    
    def testNoteSorting(self):
        measure = Measure()
        class Note(object):
            def __init__(self, start):
                self.start = start

        noteA = Note(start=5)
        noteB = Note(start=6)
        
        measure.addNote(noteB)
        measure.addNote(noteA)
        
        self.assertEqual([5, 6], [note.start for note in measure.orderedNotes()])
        
        noteC = Note(start=17)
        noteD = Note(start=1)
        measure.addNote(noteD)
        measure.addNote(noteC)
        measure.addNote(Note(start=5))
        
        self.assertEqual([1, 5, 5, 6, 17], [note.start for note in measure.orderedNotes()])

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from measure import Measure
    unittest.main()