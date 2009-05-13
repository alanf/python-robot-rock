#! /usr/bin/env python

''' testatomicparser.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Unit test for the AtomicParser class.
'''

import sys
sys.path.append('../robotrock/')

from atomicparser import *
import unittest

from score import Score
from measure import Measure
import note

class DebugReceiver(object):

	def __init__(self):
		self.events = []
	def handle(self, event):
		self.append( event )

class TestAtomicParser(unittest.TestCase):

	def testSimpleScore(self):
		"Tests the processing of score with two non-concurring notes."

		receiver = DebugReceiver()

		# m = "Dummy musician" # NO GO: staffs in score only referenced by int

		# Create a Score with a single quarter note on first beat.
		score = Score()
		measure = score.staffs[0].measures[0]
		n = note.Note(start=0, duration=note.NoteValues().QUARTER_NOTE)
		measure.addNote( n )

		# Create testing parser
		parser = AtomicParser( score=score, receiver=receiver )

		# Parse a QUARTER_NOTE's worth of the score and compare output.
		parser.onPulse( note.NoteValues().QUARTER_NOTE )
		self.assertEqual( n, receiver.events[-1] )

	def testEmptyScore(self):
		"Tests processing of an empty score."

		parser = AtomicParser( score = Score(), receiver = DebugReceiver() )

		parser.onPulse( note.NoteValues().WHOLE_NOTE )
		self.assertEqual( 0, len( receiver.events[-1] ) )

	def testEmptyStaff(self):
		"Tests processing a score with empty staffs."

		score = Score()
		dummy = score.staffs[0]
		dummy = score.staffs[1]

		receiver = DebugReceiver()

		parser = AtomicParser( score = Score(), receiver = receiver )

		parser.onPulse( note.NoteValues().WHOLE_NOTE )
		self.assertEqual( 0, len( receiver.events[-1] ) )

if __name__ == '__main__':
        unittest.main()

