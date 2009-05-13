''' testscoremarker.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Unit tests for ScoreMarker.
'''

import unittest
import sys
sys.path.append('../robotrock')
import note
from score import *

from scoremarker import ScoreMarker

class TestScoreMarker(unittest.TestCase):

	def testGetNotes(self):
		"""Tests expected results from ScoreMarker.getNotes() method."""

		# Add quarter notes at beats 1 and 2.

		first_beat = note.Note( start=0.0, duration=note.NoteValues().QUARTER_NOTE )
		score = Score()
		score.staffs[0].measures[0].addNote( first_beat )

		second_beat = note.Note( start=1.0, duration=note.NoteValues().QUARTER_NOTE )
		score.staffs[0].measures[0].addNote( second_beat )

		marker = ScoreMarker( score )

		notes = marker.getNotes( note.NoteValues().EIGHTH_NOTE )

		# Get one note...
		self.assertEquals( 1, len( notes ) )
		self.assertEquals( first_beat, notes[0] )

		# Move forward one quarter; second note should look like the first
		marker.forward( note.NoteValues().QUARTER_NOTE )
		notes = marker.getNotes( note.NoteValues().EIGHTH_NOTE )
		self.assertEquals( first_beat, notes[0] )

if __name__ == '__main__':
	unittest.main()

