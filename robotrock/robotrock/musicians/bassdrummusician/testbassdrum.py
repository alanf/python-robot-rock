#!/usr/bin/env python

''' testbassdrum.py
    Unit Tests for the BassDrum
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
import unittest
from bassdrum import BassDrum
sys.path.append('../..')
import note

# This is the test suite for the BassDrum
class TestBassdrum(unittest.TestCase):

    # Setup to allow for testing
    def setUp(self):
        
        # A stub measure to be written to for testing purposes
        class MeasureStub(object):
            def __init__(self):
                self.time_signature = (4, 4)
                self.key_signature = ('F#', 'major')
                self.notes = []
        
        self.test_measure = MeasureStub()
        self.last = MeasureStub()
        self.base = MeasureStub()
        self.highEbase = MeasureStub()
        self.lowEbase = MeasureStub()
        self._durations = note.Note.note_values

    # Tests that the BassDrum reacts appropriately to changes in energy and
    #   complexity. It does this by comparing the output of nine different
    #   state of energy and complexity against some other, previously tested
    #   states. 
    # Correct behavior is to have less notes with less energy, more notes with
    #   more energy, less off-beat notes with less complexity, and more off-beat
    #   notes with more complexity.
    # Note: Every once in a while case 3 fails, this is due to not enough
    #   off-beats.
    def testReactToChanges(self):
        # base case: energy = 50, complexity = 50
        self.drum = BassDrum()
        self.drum.compose(self.base, 0, 0, None)

        # case 1 (highEbase): energy = 80, complexity = 50
        self.drum.energy = 80
        self.drum.compose(self.highEbase, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.highEbase, self.base))
        
        # case 2 (lowEbase): energy = 20, complexity = 50
        self.drum.energy = 20
        self.drum.compose(self.lowEbase, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.base, self.lowEbase))

        # case 3: energy = 50, complexity = 80
        self.drum.complexity = 80
        self.drum.energy = 50
        self.drum.compose(self.last, 0, 0, None)
        self.assertTrue(self.compareComplexity(self.last, self.base))
        
        # case 4: energy = 80, complexity = 80
        self.drum.energy = 80
        self.drum.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.test_measure, self.last))
        self.assertTrue(self.compareComplexity(self.test_measure, self.highEbase))

        # case 5: energy = 20, complexity = 80
        self.drum.energy = 20
        self.test_measure.notes = []
        self.drum.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.last, self.test_measure))
        self.assertTrue(self.compareComplexity(self.test_measure, self.lowEbase))

        # case 6: energy = 50, complexity = 20
        self.drum.complexity = 20
        self.drum.energy = 50
        self.last.notes = []
        self.drum.compose(self.last, 0, 0, None)
        self.assertTrue(self.compareComplexity(self.base, self.last))
        
        # case 7: energy = 80, complexity = 20
        self.drum.energy = 80
        self.test_measure.notes = []
        self.drum.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.test_measure, self.last))
        self.assertTrue(self.compareComplexity(self.highEbase, self.test_measure))
        
        # case 8: energy = 20, complexity = 20
        self.drum.energy = 20
        self.test_measure.notes = []
        self.drum.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.last, self.test_measure))
        self.assertTrue(self.compareComplexity(self.lowEbase, self.test_measure))

# Helper methods:
    # Counts the number of notes in the given measure.
    def countNotes(self, measure):
        return len(measure.notes)

    # Returns whether first contains more notes than second. Both first and
    #   second need to be measures.
    def compareEnergy(self, first, second):
        return self.countNotes(first) >= self.countNotes(second)

    # Counts the number of notes not on the main beat in the given measure
    # Accomplishes this by subtracting the number of on-beats from the total
    #   number of beats.
    def countOffnotes(self, measure):
        onbeats = 0
        for x in range(len(measure.notes)):
            note = measure.notes[x]

            # Note's start is on a beat
            if (note.start % self._durations.QUARTER_NOTE) == 0:
                onbeats += 1
        return len(measure.notes) - onbeats

    # Returns whether first is more complex than second. Both first and
    #   second need to be measures.
    def compareComplexity(self, first, second):
        valueFirst = float(self.countOffnotes(first))/float(self.countNotes(first))
        valueSecond = float(self.countOffnotes(second))/float(self.countNotes(second))
        return valueFirst >= valueSecond

# Start running the tests. 
if __name__ == '__main__':
    unittest.main()
