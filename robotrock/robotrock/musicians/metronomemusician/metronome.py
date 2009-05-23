
''' musicianStructured.py
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

#definition of the recommended musician structure.
#note: one does NOT have to follow this structure to make a working musician
#note: the default musician is a metronome as defined below
class Metronome(MusicianStructured):

    #initialize the general musician
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        MusicianStructured.__init__(self, energy, complexity, time, key)
        self.instrument = 'metronome'
        self._my_tone=DrumKit["claves"]

    #determines if new music needs to be generated
    def _decide(self):
        return self._changed

    #determines what is going to be played in this measure
    #defualted to be a metronome
    def _write(self):
        for x in range(self._time[0]):
            self._addNote(x, self._my_tone)

