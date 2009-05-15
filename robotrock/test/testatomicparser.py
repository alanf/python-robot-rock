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
from dynamics import *
import note

class DebugReceiver(object):

	def __init__(self):
		self.events = []
	def handle(self, event):
		self.events.append( event )

class TestAtomicParser(unittest.TestCase):

	def testSimpleScore(self):
		"Tests the processing of score with two non-concurring notes."

		receiver = DebugReceiver()

		# m = "Dummy musician" # NO GO: staffs in score only referenced by int

		# Create a Score with a single quarter note on first beat.
		score = Score()
		measure = score.staffs[0].measures[0]
		measure.time_signature = (4,4)
		n = note.Note(start=0, tone=('C',4), duration=note.NoteValues().QUARTER_NOTE, dynamic=MEZZOFORTE)
		measure.addNote( n )

		# Create testing parser
		parser = AtomicParser( score=score, receiver=receiver )

		# Parse a QUARTER_NOTE's worth of the score and compare output.
		for i in xrange( note.NoteValues().QUARTER_NOTE / ATOMIC_NOTE ):
			parser.onPulse( ATOMIC_NOTE )

		# TODO Expected tuple will change after BETA
		actual_staff, actual_type, actual_tone, actual_dynamic = receiver.events[-1]

		self.assertEqual( score.staffs[0], actual_staff )
		self.assertEqual( "Note on", actual_type )
		self.assertEqual( n.tone, actual_tone )
		self.assertEqual( n.dynamic, actual_dynamic )

	def testEmptyScore(self):
		"Tests processing of an empty score."

		score = Score()

		parser = AtomicParser( score = score, receiver = DebugReceiver() )

		# Test a whole note's worth of score.
		for i in xrange( note.NoteValues().WHOLE_NOTE / ATOMIC_NOTE ):
			parser.onPulse( ATOMIC_NOTE )
		self.assertEqual( 0, len( receiver.events[-1] ) )

	def testEmptyStaff(self):
		"Tests processing a score with empty staffs."

		score = Score()
		dummy = score.staffs[0]

		receiver = DebugReceiver()

		parser = AtomicParser( score = Score(), receiver = receiver )

		# Test a whole note's worth of score.
		for i in xrange( note.NoteValues().WHOLE_NOTE / ATOMIC_NOTE ):
			parser.onPulse( ATOMIC_NOTE )

		self.assertEqual( 0, len( receiver.events[-1] ) )

if __name__ == '__main__':
        unittest.main()

