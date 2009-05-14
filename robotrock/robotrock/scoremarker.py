''' scoremarker.py
    Author:
    ScoreMarker is used to obtain relative note data from a mutable
    location within a Score.
'''
import copy
import note


class ScoreMarker(object):
    """Keeps a position within a score and may be moved in arbitrary
    directions.
    
    The ScoreMarker makes it possible to extract relative note data
    from a location without having to explicitly handle measure boundaries
    and other underlying Score structure."""
    
    def __init__(self, score):
        "Constructor. Creates marker into the given Score."
        self.score_slices = score.score_slices
        # Start by moving to the first measure (score_slices starts on index -1).
        self.score_slices.current_index += 1 
        self.measure_position = 0
    
    def rewind(self, n_beats):
        "Moves backward by the specified number of quarter notes."
        self.measure_position -= n_beats
        
        while self.measure_position < 0:
            self.measure_position += self.beatsInCurrentMeasure()
            self.score_slices.current_index -= 1
    
    def forward(self, n_beats):
        "Moves forward by the specified number of quarter notes."
        self.measure_position += n_beats
        
        while self.measure_position >= self.beatsInCurrentMeasure():
            self.measure_position -= self.beatsInCurrentMeasure()
            self.score_slices.current_index += 1

    def beatsInCurrentMeasure(self):
        ''' Uses a quarter note to define a full beat, to indicate how
        much total "space" there is in a measure. This way we keep our
        place when we advance through a measure before reaching the next
        measure in the staff.'''
        return self.score_slices.current()[0].time_signature[0] * \
                note.Note.note_values.QUARTER_NOTE
    
    def getNotes(self, window_size):
        """Returns the notes in the range for all staffs.
        
        The dictionary returned uses the staff as a key and an ordered
        list of time and note events as the values.  The time events
        are relative to the marker.
        
        The marker is not advanced."""
        note_events = {}
        
        measures_slice = self.score_slices.current()
        
        for measure in measures_slice:
            note_events[measure.parent] = []
            for note in measure.orderedNotes():
                if self.measure_position <= note.start \
                        < self.measure_position + window_size:
                    note_copy = copy.copy(note)
                    note_copy.start -= self.measure_position
                    note_events[measure.parent].append(note_copy)
        
        return note_events

