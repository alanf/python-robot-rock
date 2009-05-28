''' basescoremarker.py
    Author: Alan Fineberg (af@cs.washington.edu)
    BaseScoreMarker is used to obtain relative note data from a mutable
    location within a Score.
'''
import copy
import note
import scoreslice

class BaseScoreMarker(object):
    """Keeps a position within a score and may be moved in arbitrary
    directions.
    
    The ScoreMarker makes it possible to extract relative note data
    from a location without having to explicitly handle measure boundaries
    and other underlying Score structure."""
    
    def __init__(self, score):
        "Constructor. Creates marker into the given Score."
        self.score = score
        self.score_slices = scoreslice.ScoreSlice(score.staffs)
        # Start by moving to the first measure (score_slices starts on index -1).
        self.measure_position = 0
        # Assume 4 beats in measure by default. This should be updated as we advance.
        self.beats_in_measure = 4
    
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
            #self.score_slices.current_index += 1

    def beatsInCurrentMeasure(self):
        ''' Uses a quarter note to define a full beat, to indicate how
        much total "space" there is in a measure. This way we keep our
        place when we advance through a measure before reaching the next
        measure in the staff.'''
        beats = self.beats_in_measure
        for measure in self.score_slices.current():
            # If a staff no longer has a musician, it may not have a time
            # signature attribute. Search for one, or use our previous value.
            try:
                beats = measure.time_signature[0]
                break
            except AttributeError:
                continue
                
        self.beats_in_measure = beats * note.Note.note_values.QUARTER_NOTE
        return self.beats_in_measure
            
    def _updatePosition(self):
        if self.measure_position == 0:
            self.score_slices.current_index += 1
