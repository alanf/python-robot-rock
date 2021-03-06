#!/usr/bin/env python

''' testmusician.py
    Unit Tests for a musician
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import unittest
import sys
from musicianstructured import MusicianStructured
sys.path.append('../..')
import tone

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

        # Compose a measure
        self.musician.compose(self.test_measure, 0, 0, None)
        self.assertNotEqual([], self.test_measure.notes)

        # Check that all of the notes in _plans show up in the measure
        #   in the proper place (in time).
        # Iterate over _plans
        listing = self.musician._plans.keys()
        for x in listing:
            self.assertTrue(x >= 0)
            # Iterate over notes at this point in the measure
            notelisting = self.musician._plans[x]
            for y in range(len(notelisting)):
                test = False
                # Iterate over the notes printed to the measure
                for z in range(len(self.test_measure.notes)):
                    # Check that the note in _plans is in the measure
                    if self.test_measure.notes[z] == notelisting[y]:
                        test = True
                self.assertNotEqual(test, False)

    # Tests that the musician can write a chord correctly
    def testChords(self):
        self.musician = MusicianStructured()
        self.musician._plans = {}

        for key in tone._TONE_VALUE.keys():
            self.musician._addChord(0, (key,4), 'major')
            self.assertNotEqual({}, self.musician._plans)

            # Iterate over _plans
            #listing = 
            for x in self.musician._plans.keys():
                self.assertTrue(x >= 0)
                # Iterate over the notes at this point in the measure
                notelisting = self.musician._plans[x]
                test1 = test2 = test3 = False
                for y in range(len(notelisting)):
                    # Check that all the notes in the chord are present
                    if notelisting[y].tone[0] == key:
                        test1 = True
                    elif notelisting[y].tone[0] == tone.getTone((key, 4), tone.MEDIANT)[0]:
                        test2 = True
                    elif notelisting[y].tone[0] == tone.getTone((key, 4), tone.DOMINANT)[0]:
                        test3 = True
                self.assertTrue(test1)
                self.assertTrue(test2)
                self.assertTrue(test3)

# Start running the tests. 
if __name__ == '__main__':
    unittest.main()
