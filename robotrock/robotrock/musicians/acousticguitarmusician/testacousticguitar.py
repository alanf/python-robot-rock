#!/usr/bin/env python

''' testacousticguitar.py
    Unit Tests for the AcousticGuitar
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
import unittest
from acousticguitar import AcousticGuitar
sys.path.append('../..')
import note
import chords

# This is the test suite for the AcousticGuitar
class TestAcousticGuitar(unittest.TestCase):

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

    # Tests that the AcousticGuitar reacts appropriately to changes in energy and
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
        self.guitar = AcousticGuitar()
        self.guitar.compose(self.base, 0, 0, None)

        # case 1 (highEbase): energy = 80, complexity = 50
        self.guitar.energy = 80
        self.guitar.compose(self.highEbase, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.highEbase, self.base))
        
        # case 2 (lowEbase): energy = 20, complexity = 50
        self.guitar.energy = 20
        self.guitar.compose(self.lowEbase, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.base, self.lowEbase))

        # case 3: energy = 50, complexity = 80
        self.guitar.complexity = 80
        self.guitar.energy = 50
        self.guitar.compose(self.last, 0, 0, None)
        self.assertTrue(self.compareComplexity(self.last, self.base))
        
        # case 4: energy = 80, complexity = 80
        self.guitar.energy = 80
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.test_measure, self.last))
        self.assertTrue(self.compareComplexity(self.test_measure, self.highEbase))

        # case 5: energy = 20, complexity = 80
        self.guitar.energy = 20
        self.test_measure.notes = []
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.last, self.test_measure))
        self.assertTrue(self.compareComplexity(self.test_measure, self.lowEbase))

        # case 6: energy = 50, complexity = 20
        self.guitar.complexity = 20
        self.guitar.energy = 50
        self.last.notes = []
        self.guitar.compose(self.last, 0, 0, None)
        self.assertTrue(self.compareComplexity(self.base, self.last))
        
        # case 7: energy = 80, complexity = 20
        self.guitar.energy = 80
        self.test_measure.notes = []
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.test_measure, self.last))
        self.assertTrue(self.compareComplexity(self.highEbase, self.test_measure))
        
        # case 8: energy = 20, complexity = 20
        self.guitar.energy = 20
        self.test_measure.notes = []
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertTrue(self.compareEnergy(self.last, self.test_measure))
        self.assertTrue(self.compareComplexity(self.lowEbase, self.test_measure))

    # Tests that the chords are going through progressions.
    def testProgressions(self):
        self.guitar = AcousticGuitar(energy = 80, complexity = 80)
        self.assertEqual(self.guitar._energy, 80)
        self.assertEqual(self.guitar._complexity, 80)

        # First measure
        self.test_measure.notes = []
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertNotEqual(self.test_measure.notes, [])
        self.assertTrue(self.checkChords([], self.test_measure.notes, 0))
        
        # Second measure
        last_measure = self.test_measure
        self.test_measure.notes = []
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertNotEqual(self.test_measure.notes, [])

        # Third measure
        last_measure = self.test_measure
        self.test_measure.notes = []
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertNotEqual(self.test_measure.notes, [])

        # Fourth measure
        last_measure = self.test_measure
        self.test_measure.notes = []
        self.guitar.compose(self.test_measure, 0, 0, None)
        self.assertNotEqual(self.test_measure.notes, [])

# Helper methods:
    # Counts the number of notes in the given measure.
    def countNotes(self, measure):
        return (len(measure.notes)/3)

    # Returns whether first contains more notes than second. Both first and
    #   second need to be measures.
    def compareEnergy(self, first, second):
        return self.countNotes(first) > self.countNotes(second)

    # Calculates the complexity of the given measure. This is determined as the
    #   sum of how many notes are played that are not on the beat and how many
    #   on-beat notes are dropped.
    def countComplexity(self, measure):
        noteStarts = []
        for x in range(len(measure.notes)):
            note = measure.notes[x]

            # Note's start is divisible by a SIXTEENTH_NOTE
            if (note.start % self._durations.SIXTEENTH_NOTE) == 0:
                # If there is not already a note recorded at this location
                #   in the measure, then record one
                if noteStarts.count(note.start) == 0:
                    noteStarts.append(note.start)
        result = (len(measure.notes)/3) - len(noteStarts)
        # If enough notes have been played to consider drops as part of
        #   complexity, then include drops
        if (len(measure.notes)/3) > 13:
           result += (measure.time_signature[0]*4) - len(noteStarts)
        return result

    # Returns whether first is more complex than second. Both first and
    #   second need to be measures.
    def compareComplexity(self, first, second):
        valueFirst = float(self.countComplexity(first))/float(self.countNotes(first))
        valueSecond = float(self.countComplexity(second))/float(self.countNotes(second))
        return valueFirst >= valueSecond

    # Returns if the given measure(s) are written with proper chord progressions.
    #   That is, it returns True if there are no violations of chord progressions
    #   and False if it finds a violation of a chord progression. last_measure is
    #   the old measure composed, in case it contains part of a running chord
    #   progression. It is assumed that last_measure has already been checked and
    #   is correct. measure is the most recently composed measure, the one being
    #   checked. index is the start of the most recently known chord. For this test,
    #   it is assumed that the time signature is 4/4, so an index of 0 or 1 means
    #   that last_measure can be ignored, and an index of 2 or 3 means part of the
    #   chord is in the last_measure. Note, check chord only checks one chord
    #   progression, so there will need to be mulitple calls on checkChord for each
    #   measure composed.
    # Note: last_measure and measure are note lists.
    # Note: passing in [] for last_measure indicates that the chord progression
    #   starts in measure
    def checkChords(self, last_measure, measure, index):
        # Find the leading chord of the chord progression being played
        chord = self.getChord(last_measure, measure, index)
        if not(chord):
            return False
        progression = chords.Progressions[chord]
        index_start = index
        index_end = (index+2) % 4
        # Index is into measure
        if (index <= 1 or last_measure == []):
            if index_end > 3:
                index_end = 3
        # Index is into last_measure
        else:
            index_start = 0
            index_end = (index+2) % 4
        
        result = True
        # Check that all notes within the progression follow the progression
        for x in range(index_start, index_end + 1):
            # Iterate over all notes
            for y in range(len(measure)):
                # The chord for this note is known, check it
                if (measure[y].start / self._durations.QUARTER_NOTE) == x:
                    chord = chords.Majors[progression[x-index_start]]
                    if chord.count(measure[y].tone[0]) == 0:
                        result = False
        return result
            

    # Returns the leading chord of the present chord progression. Returns false
    #   if one is not found.
    def getChord(self, last_measure, measure, index):
        # If the start of the chord is in measure
        if index <= 1 or last_measure == []:
            # Iterate through all notes until a note with the start chord is found
            for x in range(len(measure)):
                if (measure[x].start / self._durations.QUARTER_NOTE) == index:
                    return measure[x].tone[0]
            else:
                return False
        # If the start of the chord is in last_measure
        else:
            # Iterate through all notes until a note with the start chord is found
            for x in range(len(last_measure)):
                if (last_measure[x].start / self._durations.QUARTER_NOTE) == index:
                       return last_measure[x].tone[0]
            else:
                return False
            
        

# Start running the tests. 
if __name__ == '__main__':
    unittest.main()
