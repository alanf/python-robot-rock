#!/usr/bin/env python

''' testmusician.py
    Unit Tests for a musician
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
import unittest
from metronome import Metronome

#definition of the test suite for musicians in general
class TestMetronome(unittest.TestCase):

    #setup to allow for testing the output of a musician
    def setUp(self):

        #a stub measure to be written to for testing purposes
        class MeasureStub(object):
            def __init__(self):
                self.time_signature = (4, 4)
                self.key_signature = ('F#', 'major')
                self.notes = []

        self.test_measure = MeasureStub()
        
    #tests that the musician is writing the music to the measure properly
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
                self.assertNotEqual(test, False)

if __name__ == '__main__':
    unittest.main()
