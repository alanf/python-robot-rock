''' musicianStructured.py
    musician definition
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
from musician import Musician
sys.path.append('../..')
import note
import dynamics
import chords

# This is the definition of MusicianStructued, the superclass of how
#   musicians are recommendedly implemented. Please see pre-existing
#   musicians and the online API for further information and techniques.
# Note: One does NOT have to follow this structure to make a working musician.
# Note: The default musician is a metronome as defined below (for testing)
class MusicianStructured(Musician):

    # Initialization of the data most to all musicians need
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        self._energy = energy
        self._complexity = complexity
        self._my_tone= ("A", 4)
        self._notes = 0
        self.instrument = 'none'
        self._key = key
        self._time = time
        self._plans = {}
        self._durations = note.Note.note_values
        self._changed = True
        # If a change is made to relevant variables, _changed should be set
        #   to True, otherwise _changed should be False. This is not a
        #   requirement, but a suggestion.        

    # This method is called by the conductor whenever any musician needs to
    #   compose music. There are three parameters: measure, window_start,
    #   and window_duration.
    # measure is a measure in the score which is handed to the musician to
    #   be filled.
    # window_start is the start index in the given measure of notes which
    #   must be composed by the time this iteration finishes.
    # window_duration is the length of the measure after window_start which
    #   needs to be composed in this iteration. This is the last chance the
    #   musician will get to edit this point in the measure and still have
    #   it be played.
    # Note: This structuring of musicians usually ignores window_start and
    #   window_duration, they are mainly for musicians which choose to
    #   compose in real-time. 
    def compose(self, measure, window_start, window_duration, current_score_slice):
        if not(self._time == measure.time_signature):
            self._time = measure.time_signature
            self._changed = True
        if not(self._key == measure.key_signature):
            self._key = measure.key_signature
            self._changed = True
        if measure.notes == [] or window_start == 0:
            self._changed = True
            
        if self._decide():
            measure.notes = []
            self._write()
            self._print(measure)

    # This method prints from _plans to the given measure. _plans is the
    #   internal data structure used to hold notes before they are added
    #   to the official measure. This allows for easier editing and single
    #   point additions to the measure which provides simplicity of code.
    # The structure of _plans is a tuple of (number, list of (notes)). 
    def _print(self, measure):
        listing = self._plans.keys()
        for x in listing:
            notelisting = self._plans[x]
            measure.notes.extend(notelisting)

    # This method calculates the start location of a note so that it is 
    #   understandable by the rest of the program given val which is the
    #   start location given as a floating point.
    # val has the following format (x.y):
    #   x is one less then the beat which the note is played in. For example:
    #   1.y plays in beat 2 and 5.y plays in beat 6.
    #   y is how far through the beat the note is played. For example: 1.5 is
    #   & of 2 and 5.125 is the e of 6. In other words, 1.5 is half way between
    #   beats 2 and 3 (an eighth beat after 2) and 5.125 is a quarter of the way
    #   between beats 6 and 7 (a sixteenth beat after 6).
    # Note: This is a helper method useful for all musicians. It is common
    #   code. No musician is required to use it, but it is recommended.
    def _getStart(self, val):
        # Finds out what how many beats have passed
        (val, remainder) = self.__shave(val, 1)
        result = val * self._durations.QUARTER_NOTE
        val = remainder

        # Finds out how much of the beat has passed (if any) if an integer
        #   multiple of a sixty-fourth note has passed.
        if not(val % .0625):
            (val, remainder) = self.__shave(val, .0625)
            result += val * self._durations.SIXTYFOURTH_NOTE

        # Finds out how much of the beat has passed (if any) if an integer
        #   multiple of a triplet note has passed. (UNTESTED)
        else:
            (val, remainder) = self.__shave(val, .33)
            result += val * self._durations.EIGHTH_NOTE_TRIPLET
        
        return result

    # This method seperates the divisible and remainder parts of val compared
    #   to amount. So val should return as an integer equal to how many times
    #   amount can go into the start val. Also, remainder is the floating point
    #   remainder such that val + remainder should equal the original val.
    # Note: This is a helper method to _getStart and should NOT be edited, or
    #   used by any other method.
    def __shave(self, val, amount):
        remainder = val % amount
        val -=remainder
        val = int(val/amount)
        return (val, remainder)

    # The getter property for energy
    @property
    def energy(self):
        return self._energy

    # The setter property for energy
    @energy.setter
    def energy(self, value):
        self._energy = value
        self._changed = True

    # The getter property for complexity
    @property
    def complexity(self):
        return self._complexity

    # The setter property for complexity
    @complexity.setter
    def complexity(self, value):
        self._complexity = value
        self._changed = True

    # The getter property for the time signature
    @property
    def time(self):
        return self._time

    # The setter property for the time signature
    @time.setter
    def time(self, value):
        self._time = value
        self._changed = True

    # The getter property for the key signature 
    @property
    def key(self):
        return self._key

    # The setter property for the key signature 
    @key.setter
    def key(self, value):
        self._key = value
        self._changed = True

    # This method adds a note to the internal data structure _plans based on
    #   the given location and tone.
    # location is the location in the measure at which the new note is to begin.
    # tone in the tone the note will have when played.
    # Note: Notes are defaulted to be a QUARTER_NOTE in length and have a dynamic
    #   of Forte. All parameters can be changed later.
    # Note: This method decrements _notes by one to indicate that a notes has
    #   been added to the measure.
    def _addNote(self, location, my_tone):
        myNote = note.Note(tone=my_tone, start=self._getStart(location), duration=self._durations.QUARTER_NOTE, rest=False, dynamic=dynamics.FORTE)
        if self._plans.keys().count(location):
            self._plans[location].append(myNote)
        else:
            self._plans[location] = [myNote]
        self._notes-=1

    # This method adds a chord to the internal data structure _plans based on
    #   the given location, chord, and chordlist.
    # location is the location in the measure at which the new note is to begin.
    # chord is an index into the given chordlist.
    # chordlist is a listing of types of chords, such as major chords, minor, etc.
    # Note: This method manages _notes so that each chord counts as only one note
    #   (aka, _notes will only be deremented by 1 after calling _addChord)
    # Note: This method uses _addNote to add notes to _plans
    def _addChord(self, location, chord, chordlist):
        self._notes += 2
        listing = chords.Majors[chord]
        if chordlist == 'minor':
            listing = Minors[chord]
        if chordlist == 'diminished':
            listing = Diminished[chord]
        if chordlist == 'augmented':
            listing = Augmented[chord]
        for x in range(len(listing)):
            tone = (listing[x], 4)
            self._addNote(location, tone)        

    # The functions below should be overwritten by the individual musicians.
    # These functions are defined at present to be for a metronome for testing
    #   purposes.

    # This method decides if new music needs to be composed on this iteration.
    # It returns a boolean True when music needs to be composed, or False when
    #   it does not.
    def _decide(self):
        return self._changed

    # This method decides what will be played this iteration. Unless compose
    #   is overwritten, _write only gets called if _decide returns true.
    #   Basically this method adds and edits the notes which will be played. 
    def _write(self):
        for x in range(self._time[0]):
            self._addNote(x, self._my_tone)

