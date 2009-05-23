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
        # Goal of reasoning:
        #   That all notes within the given time window are returned for each staff, 
        # in an order sorted by start time.
        
        # PRECONDITIONS:
        # window_size > 0
        # score.slices.current() returns a measures with count >= 0.
            # We rely on each measure having a valid parent reference.        
            # Each note has a .start >= 0, and a .duration > 0.
        # We have a measure_position reference, and it is >= 0.
        measures_slice = self.score_slices.current()
        
        note_events = {}
        # If no measures exists, this loop is not entered and we return the empty dictionary.
        for measure in measures_slice:
            # If we reach this, we have at least one measure available to read.
            # This measure has one parent, a staff, all notes processed in this
            # loop will belong to the same staff.
            note_events[measure.parent] = []
            # We don't rely on each measure having notes, but if not orderedNotes()
            # returns an empty list.
            for note in measure.orderedNotes():
                # Selects a note if its start is at or after our position, and
                # its start comes before the total size of the window we inspect.
                # Because the notes are sorted, when the inclusive notes are appended
                # to the list they, too, will be in sorted order.
                if self.measure_position <= note.start \
                        < self.measure_position + window_size:
                    # This preserves our invariant: no external objects mutated.
                    note_copy = copy.copy(note)
                    # We know this is >= 0 because of our if loop conditions.
                        # note.start >= self.measure_position
                    # Note that no original copy is mutated.
                    note_copy.start -= self.measure_position
                    
                    note_events[measure.parent].append(note_copy)

        return note_events
        # POSTCONDITIONS
        # No referenced data structures were mutated
        # At a minimum, a blank list is returned.
        # For each staff, the note list is in order by .start value.