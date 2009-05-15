#!/usr/bin/env python

''' testhanddrum.py
    Unit Tests for the HandDrum
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''


import sys
import unittest

#definition of the test suite for handdrums in specific
class TestHanddrum(unittest.TestCase):

    #general initilization
    def setUp(self):
        self.drum = HandDrum()
        
        #a stub measure to be written to for testing purposes
        class MeasureStub(object):
            def __init__(self):
                self.time_signature = (4, 4)
                self.key_signature = ('F#', 'major')
                self.notes = []

        self.test_measure = MeasureStub()
        self.test_measure2 = MeasureStub()
        self.test_measure3 = MeasureStub()
        self.test_measure4 = MeasureStub()
        self.last = MeasureStub()
        self.last2 = MeasureStub()
        self.base = MeasureStub()
        self.base2 = MeasureStub()
        self.base3 = MeasureStub()
        self._durations = note.Note.note_values

    #tests initilization settings
    def testInit(self):
        #ititialize with no inputs, test settings
        self.drum = HandDrum()
        self.assertEqual(50, self.drum.energy)
        self.assertEqual(50, self.drum.complexity)
        self.assertEqual((4,4), self.drum.time)
        self.assertEqual(('B', 'major'), self.drum.key)
        self.assertEqual(True, self.drum._changed)

        #ititialize with energy and complexity inputs, test settings
        self.drum = HandDrum(40, 80)
        self.assertEqual(40, self.drum.energy)
        self.assertEqual(80, self.drum.complexity)
        self.assertEqual((4,4), self.drum.time)
        self.assertEqual(('B', 'major'), self.drum.key)
        self.assertEqual(True, self.drum._changed)

        #ititialize with energy input, test settings
        self.drum = HandDrum(42)
        self.assertEqual(42, self.drum.energy)
        self.assertEqual(50, self.drum.complexity)
        self.assertEqual((4,4), self.drum.time)
        self.assertEqual(('B', 'major'), self.drum.key)
        self.assertEqual(True, self.drum._changed)

    #tests that the handdrum is composing and storing properly
    def testWrite(self):
        self.drum._write()
        self.assertNotEqual({}, self.drum._plans)

    #tests that the handdrum is writing the music to the measure properly
    def testCompose(self):    
        self.drum.compose(self.test_measure, 0, 0)
        self.assertNotEqual({}, self.drum._plans)
        self.assertNotEqual([], self.test_measure.notes)

        listing = self.drum._plans.keys()
        for x in listing:
            self.assertNotEqual(0, x)
            test = False
            for y in range(len(self.test_measure.notes)):
                if self.test_measure.notes[y] == self.drum._plans[x]:
                    test = True
            self.assertNotEqual(test, False)
        
    #tests that the handdrum outputs something different
    #when the energy and complexity change, and that it
    #reacts appropriately (ex. less notes for less energy)
    def testReactToChanges(self):
        #base case: energy = 50, complexity = 50
        self.drum = HandDrum()
        self.drum.compose(self.base, 0, 0)

        #case 1: energy = 80, complexity = 50
        self.drum.energy = 80
        self.drum.compose(self.base2, 0, 0)
        self.assertTrue(self.compareEnergy(self.base2, self.base))
        
        #case 2: energy = 20, complexity = 50
        self.drum.energy = 20
        self.drum.compose(self.base3, 0, 0)
        self.assertTrue(self.compareEnergy(self.base, self.base3))

        #case 3: energy = 50, complexity = 80
        self.drum.complexity = 80
        self.drum.energy = 50
        self.drum.compose(self.last, 0, 0)
        self.assertTrue(self.compareComplexity(self.last, self.base))
        
        #case 4: energy = 80, complexity = 80
        self.drum.energy = 80
        self.drum.compose(self.test_measure, 0, 0)
        self.assertTrue(self.compareEnergy(self.test_measure, self.last))
        self.assertTrue(self.compareComplexity(self.test_measure, self.base2))

        #case 5: energy = 20, complexity = 80
        self.drum.energy = 20
        self.drum.compose(self.test_measure2, 0, 0)
        self.assertTrue(self.compareEnergy(self.last, self.test_measure2))
        self.assertTrue(self.compareComplexity(self.test_measure2, self.base3))

        #case 6: energy = 50, complexity = 20
        self.drum.complexity = 20
        self.drum.energy = 50
        self.drum.compose(self.last2, 0, 0)
        self.assertTrue(self.compareComplexity(self.base, self.last2))
        
        #case 7: energy = 80, complexity = 20
        self.drum.energy = 80
        self.drum.compose(self.test_measure3, 0, 0)
        self.assertTrue(self.compareEnergy(self.test_measure3, self.last2))
        self.assertTrue(self.compareComplexity(self.base2, self.test_measure3))
        
        #case 8: energy = 20, complexity = 20
        self.drum.energy = 20
        self.drum.compose(self.test_measure4, 0, 0)
        self.assertTrue(self.compareEnergy(self.last2, self.test_measure4))
        self.assertTrue(self.compareComplexity(self.base3, self.test_measure4))

#helper methods:
    #counts the number of notes in the given measure
    def countNotes(self, measure):
        return len(measure.notes)

    #returns whether first contains more notes than second
    def compareEnergy(self, first, second):
        return self.countNotes(first) > self.countNotes(second)

    #counts the number of notes not on the main beat in the given measure
    def countOffnotes(self, measure):
        onbeats = 0
        for x in range(len(measure.notes)):
            note = measure.notes[x]
            #print 'here is a note', note.__dict__
            #notes duration is either an eigth not or quarter note
            if (note.start % self._durations.QUARTER_NOTE) == 0:
                onbeats += 1
        return len(measure.notes) - onbeats

    #returns whether first is more complex than second
    def compareComplexity(self, first, second):
        valueFirst = float(self.countOffnotes(first))/float(self.countNotes(first))
        valueSecond = float(self.countOffnotes(second))/float(self.countNotes(second))
        return valueFirst >= valueSecond

        

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from handdrum import HandDrum
    import note
    unittest.main()
