''' metronome.py
    musician definition
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
sys.path.append('../shared')
from musicianstructured import MusicianStructured
sys.path.append('../..')
from drumkit import DrumKit
import note
import dynamics

# This is the definition of a metronome based on MusicianStructured.
class Metronome(MusicianStructured):

    # Intialize the metronome specific values, all else is done by the super
    #   class __init__ method. 
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        MusicianStructured.__init__(self, energy, complexity, time, key)
        self.instrument = 'metronome'
        self._my_tone=DrumKit["claves"]

    # This method decides if new music needs to be composed on this iteration.
    # It returns a boolean True when music needs to be composed, or False when
    #   it does not.
    def _decide(self):
        return self._changed

    # This method decides what will be played this iteration.
    # For a metronome, that is a note on every beat and only every beat.
    def _write(self):
        for x in range(self._time[0]):
            self._addNote(x, self._my_tone)

# Returns the constructor for a Metronome.
def Musician():
    return Metronome()

