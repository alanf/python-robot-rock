''' scoremarker.py
    Author:
    ScoreMarker is used to obtain relative note data from a mutable
    location within a Score, and return notes to a score parser.
'''
import copy
import note
import basescoremarker

class ScoreMarker(basescoremarker.BaseScoreMarker):
    def getNotes(self, window_size):
        """Returns the notes in the range for all staffs.
        
        The dictionary returned uses the staff as a key and an ordered
        list of time and note events as the values.  The time events
        are relative to the marker.
        
        The marker is not advanced."""
        self._updatePosition()
        
        measures_slice = self.score_slices.current()
        
        note_events = {}
        for measure in measures_slice:
            note_events[measure.parent] = []
            for note in measure.orderedNotes():
                if self.measure_position <= note.start \
                        < self.measure_position + window_size:
                    note_copy = copy.copy(note)
                    note_copy.start -= self.measure_position
                    note_events[measure.parent].append(note_copy)

        return note_events
