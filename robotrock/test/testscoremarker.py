# testscoremarker.py

import unittest
import sys
sys.path.append('../robotrock')
import note

from scoremarker import ScoreMarker

class TestScoreMarker(unittest.TestUnit):

	def testGetNotes(self):

		# Add quarter notes at beats 1 and 2.

		first_beat = note.Note( start=0.0, duration=note.getValues().QUARTER_NOTE )
		score = Score[0].measures[0].AddNote( n )

		second_beat = note.Note( start=1.0, duration=note.getValues().QUARTER_NOTE )
		score = Score[0].measures[0].AddNote( n )

		marker = ScoreMarker( score )

		notes = marker.getNotes( note.getValues().EIGHTH_NOTE )

		# Get one note...
		self.assertEquals( 1, len( notes ) )
		self.assertEquals( first_beat, notes[0] )

		# move forward; second note should look like the first
		marker.forward( note.getValues().QUARTER_NOTE )
		notes = marker.getNotes( note.getValues().EIGHTH_NOTE )
		self.assertEquals( first_beat, notes[0] )

if __name__ == '__main__':
	unittest.main()

