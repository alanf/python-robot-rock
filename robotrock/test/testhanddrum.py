#!/usr/bin/env python

''' testhanddrum.py
    Unit Tests for the HandDrum
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''


import sys
import unittest

class TestMusician(unittest.TestCase):

    def setUp(self):
        self.drum = HandDrum([])

    #tests init settings
    def testInit(self):
        self.musician = HandDrum([])
        self.assertEqual(50, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)
        
        self.musician = HandDrum([], 40, 80)
        self.assertEqual(40, self.musician.energy)
        self.assertEqual(80, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)

        self.musician = HandDrum([], 42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)

    #tests that musician outputs to a measure
    def testWrite(self):
        self.drum._write()
        #self.asserNotEqual([], getCurrentMeasure(instrument))
        self.assertNotEqual({}, self.drum._plans)
        
    #tests that the musician outputs something different
    #when the energy and complexity change, and that it
    #reacts appropriately (ex. less notes for less energy)
    def testReactToChanges(self):
        #base case: energy = 50, complexity = 50
        self.musician = HandDrum([])
        self.musician.compose()
        #self.base = getCurrentMeasure(instrument)
        self.base = self.musician.current_measure

        #case 1: energy = 80, complexity = 50
        self.musician.energy = 80
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareEnergy(self.current, self.base))
        #self.base2 = self.current
        self.assertTrue(self.compareEnergy(self.musician.current_measure, self.base))
        self.base2 = self.musician.current_measure
        
        #case 2: energy = 20, complexity = 50
        self.musician.energy = 20
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareEnergy(self.base, self.current))
        #self.base3 = self.current
        self.assertTrue(self.compareEnergy(self.base, self.musician.current_measure))
        self.base3 = self.musician.current_measure

        #case 3: energy = 50, complexity = 80
        self.musician.complexity = 80
        self.musician.energy = 50
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareComplexity(self.current, self.base))
        #self.last = self.current
        self.assertTrue(self.compareComplexity(self.musician.current_measure, self.base))
        self.last = self.musician.current_measure

        #case 4: energy = 80, complexity = 80
        self.musician.energy = 80
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareEnergy(self.current, self.last))
        #self.assertTrue(self.compareComplexity(self.current, self.base2))
        self.assertTrue(self.compareEnergy(self.musician.current_measure, self.last))
        self.assertTrue(self.compareComplexity(self.musician.current_measure, self.base2))

        #case 5: energy = 20, complexity = 80
        self.musician.energy = 20
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareEnergy(self.last, self.current))
        #self.assertTrue(self.compareComplexity(self.current, self.base3))
        self.assertTrue(self.compareEnergy(self.last, self.musician.current_measure))
        self.assertTrue(self.compareComplexity(self.musician.current_measure, self.base3))

        #case 6: energy = 50, complexity = 20
        self.musician.complexity = 20
        self.musican.energy = 50
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareComplexity(self.base, self.current))
        #self.last = self.current
        self.assertTrue(self.compareComplexity(self.base, self.musician.current_measure))
        self.last = self.musician.current_measure

        #case 7: energy = 80, complexity = 20
        self.musician.energy = 80
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareEnergy(self.current, self.last))
        #self.assertTrue(self.compareComplexity(self.base2, self.current))
        self.assertTrue(self.compareEnergy(self.musician.current_measure, self.last))
        self.assertTrue(self.compareComplexity(self.base2, self.musician.current_measure))
        
        #case 8: energy = 20, complexity = 20
        self.musician.energy = 20
        self.musician.compose()
        #self.current = getCurrentMeasure(instrument)
        #self.assertTrue(self.compareEnergy(self.last, self.current))
        #self.assertTrue(self.compareComplexity(self.base3, self.current))
        self.assertTrue(self.compareEnergy(self.last, self.musician.current_measure))
        self.assertTrue(self.compareComplexity(self.base3, self.musician.current_measure))

#helper methods:
    #counts the number of notes in the given measure
    def countNotes(self, measure):
        return 0    #FIX!!!

    #returns whether first contains more notes than second
    def compareEnergy(self, first, second):
        return self.countNotes(first) > self.countNotes(second)

    #counts the number of notes not on the main beat in the given measure
    def countOffnotes(self, meausure):
        return 0    #FIX!!!

    #returns whether first is more complex than second
    def compareComplexity(self, first, second):
        valueFirst = self.countNotes(first)/self.countOffnotes(first)
        valueSecond = self.countNotes(second)/self.countOffnotes(second)
        return valueFirst < valueSecond

        

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from musician import Musician
    from handdrum import HandDrum
    unittest.main()
