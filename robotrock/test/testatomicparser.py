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
	def onEndOfFrame(self, t):
		pass

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
		parser = AtomicParser( score=score, receivers = [ receiver ] )

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
		receiver = DebugReceiver()

		parser = AtomicParser( score = score, receivers = [ receiver ] )

		# Test a whole note's worth of score.
		for i in xrange( note.NoteValues().WHOLE_NOTE / ATOMIC_NOTE ):
			parser.onPulse( ATOMIC_NOTE )

		self.assertEqual( 0, len( receiver.events ) )

	def testEmptyStaff(self):
		"Tests processing a score with empty staffs."

		score = Score()
		dummy = score.staffs[0]

		receiver = DebugReceiver()

		parser = AtomicParser( score = Score(), receivers = [ receiver ] )

		# Test a whole note's worth of score.
		for i in xrange( note.NoteValues().WHOLE_NOTE / ATOMIC_NOTE ):
			parser.onPulse( ATOMIC_NOTE )

		self.assertEqual( 0, len( receiver.events ) )

	def testEventOrder(self):
		"Tests correcting ordering of simulataneous event generation."

		receiver = DebugReceiver()

		# Create a Score with a single quarter note on first beat.
		score = Score()
		measure = score.staffs[0].measures[0]
		staff = score.staffs[0]
		measure.time_signature = (4,4)

		qn = duration=note.NoteValues().QUARTER_NOTE
		measure.addNote( note.Note(start=0*qn, tone=('C',4), duration=qn, dynamic=MEZZOFORTE) )
		measure.addNote( note.Note(start=1*qn, tone=('E',4), duration=qn, dynamic=MEZZOFORTE) )
		measure.addNote( note.Note(start=2*qn, tone=('G',4), duration=qn, dynamic=MEZZOFORTE) )
		measure.addNote( note.Note(start=3*qn, tone=('A',4), duration=qn, dynamic=MEZZOFORTE) )

		parser = AtomicParser( score = score, receivers = [ receiver ] )

		# Test a whole note's worth of score.
		for i in xrange( note.NoteValues().WHOLE_NOTE / ATOMIC_NOTE ):
			parser.onPulse( ATOMIC_NOTE )

		parser.onPulse( ATOMIC_NOTE ) # Trigger last "Note off event"
	
		expected_values = [
			(staff, "Note on",  ('C',4), MEZZOFORTE),
			(staff, "Note off", ('C',4), MEZZOFORTE),
			(staff, "Note on",  ('E',4), MEZZOFORTE),
			(staff, "Note off", ('E',4), MEZZOFORTE),
			(staff, "Note on",  ('G',4), MEZZOFORTE),
			(staff, "Note off", ('G',4), MEZZOFORTE),
			(staff, "Note on",  ('A',4), MEZZOFORTE),
			(staff, "Note off", ('A',4), MEZZOFORTE) ]

		for i in xrange( len( receiver.events ) ):
			self.assertEqual( expected_values[i], receiver.events[i] )

if __name__ == '__main__':
        unittest.main()

