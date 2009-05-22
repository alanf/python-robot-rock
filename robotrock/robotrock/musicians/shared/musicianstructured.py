
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

#definition of the recommended musician structure.
#note: one does NOT have to follow this structure to make a working musician
#note: the default musician is a metronome as defined below
class MusicianStructured(Musician):

    #initialize the general musician
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        self._energy = energy
        self._complexity = complexity
        self._my_tone=38
        self._notes = 0
        self.instrument = 'none'
        self._key = key
        self._time = time
        self._plans = {}
        self._changed = True #if a change is made, set changed to 1
                            #set to 0 by decide method when composing
        self._durations = note.Note.note_values

    #composes to the given measure if it needs to
    #measure is the measure being composed to
    #window_start is the start of the part of the measure that needs to be composed
    #window_duration is the length of the measure that needs to be composed
    #note: this structure ignores window_start and window_duration for the most
    #   part, they are mainly for allowing musicians to run dynamically
    def compose(self, measure, window_start, window_duration): 
        if not(self._time == measure.time_signature):
            self._time = measure.time_signature
            self._changed = True
        if not(self._key == measure.key_signature):
            self._key = measure.key_signature
            self._changed = True
        if measure.notes == [] or window_start == 0:
            self._changed = True
            
        if self._decide():
            self._write()
            self._print(measure)

    #printing _plans (internal data structure) to the given measure
    def _print(self, measure):
        listing = self._plans.keys()
        for x in listing:
            notelisting = self._plans[x]
            measure.notes.extend(notelisting)

    #turns the numerical value val into a start value understandable by the
    #   score
    def _getStart(self, val):
        (val, remainder) = self.__shave(val, 1)
        result = val * self._durations.QUARTER_NOTE
        val = remainder

        if not(val % .0625):
            (val, remainder) = self.__shave(val, .0625)
            result += val * self._durations.SIXTYFOURTH_NOTE

        else:   #triplets probably dont work, untested
            (val, remainder) = self.__shave(val, .33)
            result += val * self._durations.EIGHTH_NOTE_TRIPLET
        
        return result

    #helper for _getStart, does the work of figuring out how many
    #   of this type of note need to be skipped.
    #returns (val, remainder) where val is the number of this note
    #   to be skipped and remainder is how much of the measure is
    #   left to be skipped
    def __shave(self, val, amount):
        remainder = val % amount
        val -=remainder
        val = int(val/amount)
        return (val, remainder)

    #property for energy
    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        self._changed = True

    #property for complexity
    @property
    def complexity(self):
        return self._complexity

    @complexity.setter
    def complexity(self, value):
        self._complexity = value
        self._changed = True

    #property for time
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self._changed = True

    #property for key 
    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self._changed = True

        
    #adds a note at the specified location in the measure. each note is defaulted
    #   to be a quarter note and have the dynamics of Forte, these can of course be
    #   changed later. This version assumes that _plans (the data store being written to)
    #   is a dictionary of type (num, list). 
    def _addNote(self, location, my_tone):
        myNote = note.Note(tone=my_tone, start=self._getStart(location), duration=self._durations.QUARTER_NOTE, rest=False, dynamic=dynamics.FORTE)
        if self._plans.keys().count(location):
            self._plans[location].append(myNote)
        else:
            self._plans[location] = [myNote]
        self._notes-=1

    #adds the specified chord from the specified chordlist to the specified
    #   location in the measure. it uses _addNote to do so, and also keeps
    #   _notes at the proper count (so adding a chord only takes up one note)
    #chordlist is the type of chord: major, minor, diminished, etc.
    #chord is an index into the chordlist specified
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
            self._addNote(location, listing[x])        


    #functions below should be rewritten by individual musicians

    #determines if new music needs to be generated
    def _decide(self):
        return self._changed

    #determines what is going to be played in this measure
    #defualted to be a metronome
    def _write(self):
        for x in range(self._time[0]):
            self._addNote(x, self._my_tone)

