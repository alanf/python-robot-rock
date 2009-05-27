#!/usr/bin/env python

''' testmusician.py
    Unit Tests for a musician
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import unittest
from musicianstructured import MusicianStructured

# This is the definition of the test suite for the MusicianStructured class.
#   All of the functionality of a musician is tested here (such as adding
#   notes and writing to measures). Individual style correctness is left
#   to independant musician testing. 
class TestMusician(unittest.TestCase):

    # Setup method to allow for musicians to be tested.
    def setUp(self):
        self.musician = MusicianStructured(42)

        # A stub measure to be written to for testing purposes.
        class MeasureStub(object):
            def __init__(self):
                self.time_signature = (4, 4)
                self.key_signature = ('F#', 'major')
                self.notes = []

        self.test_measure = MeasureStub()
        
    # This test tests that musicians are being initialized correctly
    def testInit(self):
        # Initialize with no inputs, then test settings
        self.musician = MusicianStructured()
        self.assertEqual(50, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual((4,4), self.musician.time)
        self.assertEqual(('B', 'major'), self.musician.key)
        self.assertEqual(True, self.musician._changed)

        # Initialize with a given setting for energy and complexity
        self.musician = MusicianStructured(40, 80)
        self.assertEqual(40, self.musician.energy)
        self.assertEqual(80, self.musician.complexity)
        self.assertEqual((4,4), self.musician.time)
        self.assertEqual(('B', 'major'), self.musician.key)
        self.assertEqual(True, self.musician._changed)

        # Initialize with a given setting for energy only
        self.musician = MusicianStructured(42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual((4,4), self.musician.time)
        self.assertEqual(('B', 'major'), self.musician.key)
        self.assertEqual(True, self.musician._changed)

    # Tests if the musician is writing to the internal data structure
    #   correctly. Tests _addNote in the process.
    def testWrite(self):
        self.musician._write()
        self.assertNotEqual({}, self.musician._plans)

    # Tests that all of the getter and setter properties are working
    #   correctly
    def testGetAndSet(self):
        # Testing engergy
        self.musician.energy = 23
        self.assertEqual(23, self.musician.energy)
        # Testing complexity
        self.musician.complexity = 78
        self.assertEqual(78, self.musician.complexity)
        # Testing time signature
        self.musician.time = (2,6)
        self.assertEqual((2,6), self.musician.time)
        # Testing key signature
        self.musician.key = ('A', 'major')
        self.assertEqual(('A', 'major'), self.musician.key)
        
    # Tests that the given measure is being written to correctly and
    #   completely.
    def testCompose(self):
        self.musician = MusicianStructured()
    
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

    # Tests that the musician can write a chord correctly
    def testChords(self):
        self.musician = MusicianStructured()
        self.musician._plans = {}
        self.musician._addChord(0, 'D', 'major')
        self.assertNotEqual({}, self.musician._plans)

        listing = self.musician._plans.keys()
        for x in listing:
            self.assertTrue(x >= 0)
            notelisting = self.musician._plans[x]
            testD = testF = testA = False
            for y in range(len(notelisting)):
                if notelisting[y].tone[0] == "D":
                    testD = True
                elif notelisting[y].tone[0] == "F#":
                    testF = True
                elif notelisting[y].tone[0] == "A":
                    testA = True
            self.assertTrue(testD and testF and testA)

# Start running the tests. 
if __name__ == '__main__':
    unittest.main()
