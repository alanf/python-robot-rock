#!/usr/bin/env python

''' testmusician.py
    Unit Tests for a musician
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import unittest
from musicianstructured import MusicianStructured

#definition of the test suite for musicians in general
class TestMusician(unittest.TestCase):

    #setup to allow for testing the output of a musician
    def setUp(self):

        #a stub measure to be written to for testing purposes
        class MeasureStub(object):
            def __init__(self):
                self.time_signature = (4, 4)
                self.key_signature = ('F#', 'major')
                self.notes = []

        self.test_measure = MeasureStub()
        
    #tests initialization settings
    def testInit(self):
        #ititialize with no inputs, test settings
        self.musician = MusicianStructured()
        self.assertEqual(50, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual((4,4), self.musician.time)
        self.assertEqual(('B', 'major'), self.musician.key)
        self.assertEqual(True, self.musician._changed)

        #initialize with given energy and complexity
        self.musician = MusicianStructured(40, 80)
        self.assertEqual(40, self.musician.energy)
        self.assertEqual(80, self.musician.complexity)
        self.assertEqual((4,4), self.musician.time)
        self.assertEqual(('B', 'major'), self.musician.key)
        self.assertEqual(True, self.musician._changed)

        #initialize with energy only
        self.musician = MusicianStructured(42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual((4,4), self.musician.time)
        self.assertEqual(('B', 'major'), self.musician.key)
        self.assertEqual(True, self.musician._changed)

    #tests the musician is composing and storing properly
    def testWrite(self):
        #check initialization
        self.musician = MusicianStructured(42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual((4,4), self.musician.time)
        self.assertEqual(True, self.musician._changed)

        #test to see if the musician is writing music
        self.musician._write()
        self.assertNotEqual({}, self.musician._plans)

    #tests that all of the properties are working properly
    def testGetAndSet(self):
        #init
        self.musician = MusicianStructured()
        #test engergy
        self.musician.energy = 23
        self.assertEqual(23, self.musician.energy)
        #test complexity
        self.musician.complexity = 78
        self.assertEqual(78, self.musician.complexity)
        #test time signature
        self.musician.time = (2,6)
        self.assertEqual((2,6), self.musician.time)
        #test key signature
        self.musician.key = ('A', 'major')
        self.assertEqual(('A', 'major'), self.musician.key)
        
    #tests that the musician is writing the music to the measure properly
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

    #tests that the musician can write a chord properly
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
                if notelisting[y].tone == "D":
                    testD = True
                elif notelisting[y].tone == "F#":
                    testF = True
                elif notelisting[y].tone == "A":
                    testA = True
            self.assertTrue(testD and testF and testA)

        

if __name__ == '__main__':
    unittest.main()
