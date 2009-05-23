''' acousticguitar.py
    definition of an acoustic guitar
    Author: Rich Snider <mrsoviet@cs.washington.edu
'''

import sys
import random
sys.path.append('../shared')
from musicianstructured import MusicianStructured
sys.path.append('../..')
import note
import dynamics
import chords


# This is the definition of an acoustic guitar
class AcousticGuitar(MusicianStructured):

    # Initialization of a AcousticGuitar. Initializes AcousticGuitar specific
    #   values and leaves the rest to the super class __init__ method.
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        MusicianStructured.__init__(self, energy, complexity, time, key)
        self.instrument = 'acousticguitar'
        self._my_tone= (key[0], 4)

    # This method decides if new music needs to be composed on this iteration.
    def _decide(self):
        return self._changed

    # This method decides what will be played this iteration. This method
    #   assumes the whole measure needs to be rebuilt, so it does so.
    # For an AcousticGuitar this is done by playing a count of notes depending
    #   on energy and dropping notes depending on complexity.
    def _write(self):
        self._plans = {}
        self._notes = self._getNotes()
        self._locations()
        self._lengths()
        self._dynamics()
        self._changed = False

    # This method calculates the number of notes to be played in this
    #   measure. This calcluation is based on the energy and complexity
    #   presently set. The number of notes played varies with the time
    #   signature. energy and complexity range from 1 to 100 (or 0 to 99)
    # Just returns 4 for this version.
    def _getNotes(self):
        # Calculates the base number of notes. At full energy, this should
        #   be 16 and should have a minimum of 2. The 21 is provided by the
        #   leading 1 and the range from 2-16 is provided by dividing energy
        #   by 6. 
        notes = 2 + self._energy/6
        # Adds notes to the number of notes to be played due to complexity.
        #   The number of notes that are added is also a function of energy.
        #   More energy means more notes, and so does more complexity. But a
        #   high complexity and low energy shouldnt add too many notes. To
        #   do this, both energy and complexity need to be in the numerator;
        #   also, something needs to be in the denominator. 100 is found to be
        #   the correct denominator because complexity == 100, energy == 0, only
        #   one note is added. However, at complexity == 100, energy == 100, 16
        #   notes are added.
        notes = notes+(self._complexity/(100/notes))
        # Modulates the number of notes based on the time signature. 
        notes = notes * self._time[0] / self._time[1]
        return 4

    # This method decides the start locations of all the notes in the to be
    #   played. It does this by splitting the job up into on-beat notes and
    #   off-beat notes. 
    def _locations(self):
        self._onbeat()
        self._offbeat()
        self._dropnotes()

    # This method decides the length of each note in the measure. For an
    #   AcousticGuitar, this is not limited. 
    def _lengths(self):
        pass

    # This method decides the dynamics of each note in the measure. Right now,
    #   everything is left to defualt (Forte).
    def _dynamics(self):
        pass

    # This method adds notes to the measure which are on the beat.
    def _onbeat(self):
        

        
        listing = chords.Progressions[self._key[0]]
        for x in range(len(listing)):
            self._addChord(x, listing[x], 'major')

    # This method adds notes to the measure which are off the beat.
    def _offbeat(self):
        pass

    # This method drops random notes from the measure based on the values
    #   of complexity.
    def _dropnotes(self):
        pass

# Returns the construtor for the HandDrum		
def Musician():
    return HandDrum()
        

    