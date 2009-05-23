#!/usr/bin/env python

''' testmusician.py
    Unit Tests for a musician
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
import unittest
from metronome import Metronome

# This is the test suite for the metronome
class TestMetronome(unittest.TestCase):

    # Setup to allow the metronome to be tested
    def setUp(self):

        # A stub measure to be written to for testing purposes
        class MeasureStub(object):
            def __init__(self):
                self.time_signature = (4, 4)
                self.key_signature = ('F#', 'major')
                self.notes = []

        self.test_measure = MeasureStub()
        
    # Tests that the metronome is only writing as a metronome. 
    def testCompose(self):
        self.musician = Metronome()
    
        self.musician.compose(self.test_measure, 0, 0)
        self.assertNotEqual([], self.test_measure.notes)

        listing = self.musician._plans.keys()
        for x in listing:
            self.assertTrue(x >= 0)
            notelisting = self.musician._plans[x]
            for y in range(len(notelisting)):
                test = False
                for z in range(len(self.test_measure.notes)):
                    if self.test_measure.notes[z] == notelisting[y]:
                        test = True
                    # Fails if there is a note played that is not on the beat
                    self.assertFalse(self.test_measure.notes[z].start % 1)
                # Fails if a note is missing from the measure that should be there
                self.assertNotEqual(test, False)

# Start running the tests. 
if __name__ == '__main__':
    unittest.main()
