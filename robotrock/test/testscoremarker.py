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
    def testBeatsInCurrentMeasure(self):
        score = Score()
        score.staffs[0].measures[0].time_signature = (4, 4)
        marker = ScoreMarker( score )
        
        self.assertEquals(marker.beatsInCurrentMeasure(), \
                note.Note.note_values.QUARTER_NOTE * 4)
                
    def testGetNotes(self):
        """Tests expected results from ScoreMarker.getNotes() method."""
        # Add quarter notes at beats 1 and 2.
        first_beat = note.Note( start=0, duration=note.Note.note_values.QUARTER_NOTE )
        score = Score()
        first_staff = score.staffs[0]
        
        first_staff.measures[0].time_signature = (4, 4)
        first_staff.measures[0].addNote( first_beat )
        
        
        second_beat = note.Note( start=note.Note.note_values.QUARTER_NOTE,\
                duration=note.Note.note_values.QUARTER_NOTE )
        first_staff.measures[0].addNote( second_beat )

        marker = ScoreMarker( score )

        notes = marker.getNotes( note.Note.note_values.EIGHTH_NOTE )
        # Get one note...
        self.assertEquals( 1, len( notes[first_staff] ) )
        
        self.assertEquals( note.Note.note_values.QUARTER_NOTE, \
                notes[first_staff][0].duration)
        self.assertEquals( 0, notes[first_staff][0].start)
        
        # Move forward one quarter; second note should look like the first
        marker.forward( note.Note.note_values.QUARTER_NOTE )
        notes = marker.getNotes( note.Note.note_values.EIGHTH_NOTE )
        self.assertEqual( 1, len( notes[first_staff] ) )

        self.assertEquals( note.Note.note_values.QUARTER_NOTE, \
                notes[first_staff][0].duration)
        self.assertEquals( 0, notes[first_staff][0].start)

if __name__ == '__main__':
    unittest.main()

