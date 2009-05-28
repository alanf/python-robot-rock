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
        self.instrument = 'jazz bass'
        self._my_tone= (key[0], 4)
        self._last_progression = []
        self._this_progression = []
        self._last_index = 0
        self._this_index = self._time[0] - 3 #starts 3 early for priming purposes

    # This method decides if new music needs to be composed on this iteration.
    def _decide(self):
        return self._changed

    # This method decides what will be played this iteration. This method
    #   assumes the whole measure needs to be rebuilt, so it does so.
    # For an AcousticGuitar this is done by playing a count of notes depending
    #   on energy and dropping notes depending on complexity.
    def _write(self):
        self._plans = {}
        self._progressions()
        self._notes = self._getNotes()
        self._locations()
        self._lengths()
        self._dynamics()
        self._changed = False

    # This method determines which chord progression will be used for this measure
    # For simplicity, a given chord is played for a beat. Also, progressions are
    #   assumed to be 3 chords in length, hence the magic number 3 everywhere.
    #   To allow for varying progression lengths, simply replace the 3's with a
    #   variable holding the progression length.
    def _progressions(self):
        # Assume this is a nw measure, 
        # Progression is used to determine the order chords were or will be played
        self._last_progression = self._this_progression
        self._this_progression = []
        # Idicies indicate the starts of of chord progressions. For simplicity,
        #   progressions are assumed to be 3 chords in length. Also, the last index
        #   + 3 will always be >= the number of beats (self._time[0]).
        self._last_index = self._this_index
        self._this_index = (self._this_index + 3) % self._time[0]
        self._time[0]
        
        # There is a progression to be finished
        if self._this_index > 0:
            #print self._last_progression
            #print self._last_index
            # Get the presently playing progression
            listing = chords.Progressions[self._last_progression[self._last_index]]
            # Iterate over the remaining chords in the progression to be finished
            y = 0
            for x in range(3-self._this_index, 3):
                self._this_progression.append(listing[x])
                y += 1

        while self._this_index < self._time[0]:
            # Choose the next progression, fill it in
            # At high complexity, the core progression should be played 1 of every
            #   4 progressions at minimum. At low complexity it should be the only
            #   progression played.
            chance = random.randrange(1+self._complexity/25)
            # A random progressoion is to be chosen (not playing the core one)
            if chance > 0:
                # Randomly choose a progression (there are 17 major progressions)
                chance = random.randrange(17)
                prog = chords.Progressions.keys()[chance]
                self._this_progression.extend(chords.Progressions[prog])
            # Play the core progression
            else:
                self._this_progression.extend(chords.Progressions[self._key[0]])
            self._this_index += 3

        # Set _this_index to be the last progression index in the measure
        self._this_index = self._time[0] - (3 - (self._this_index % self._time[0]))

        #listing = chords.Progressions[self._key[0]]
        #for x in range(len(listing)):
        #    self._addChord(x, self._this_progression[x], 'major')
        

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
        return notes

    # This method decides the start locations of all the notes in the to be
    #   played. It does this by splitting the job up into on-beat notes and
    #   off-beat notes. 
    def _locations(self):
        self._onbeat()
        if self._notes > 0:
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
        notes = self._notes
        # Iterate through all beats
        for x in range(self._time[0]):
            
            # If there are at least as many notes left to play as onbeat notes
            #   left to be played, then write all onbeat notes
            if self._notes >= 4*(self._time[0]-x):
                self._addChord(x, self._this_progression[x], 'major')
                self._addChord(x+.25, self._this_progression[x], 'major')
                self._addChord(x+.5, self._this_progression[x], 'major')
                self._addChord(x+.75, self._this_progression[x], 'major')
                
            # If there are at least as many notes to play as half of the onbeat
            #   notes left to be played, then write at least half and randomly
            #   write the other onbeat notes
            elif self._notes >= 2*(self._time[0]-x):
                self._addChord(x, self._this_progression[x], 'major')
                self._addChord(x+.5, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes * 2)
                if chance < self._notes:
                    self._addChord(x+.25, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes * 2)
                if chance < self._notes:
                    self._addChord(x+.75, self._this_progression[x], 'major')
            
            # If there are at least as many notes to play as there are beats,
            #   then play the beats and randomly play the other onbeat notes.
            elif self._notes >= self._time[0]-x:
                self._addChord(x, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes * 2)
                if chance < self._notes:
                    self._addChord(x+.5, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes * 4)
                if chance < self._notes:
                    self._addChord(x+.25, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes * 4)
                if chance < self._notes:
                    self._addChord(x+.75, self._this_progression[x], 'major')

            # There are not enough notes to play all of the beats, so play them
            #   randomly.
            else:
                chance = random.randrange(1 + self._notes * 2)
                if chance < self._notes:
                    self._addChord(x, self._this_progression[x], 'major')

        # There are still notes to be played that should be onbeat notes
        if notes <= 16 and self._notes > 0:
            x = 0
            listing = self._plans.keys()
            while self._notes > 0:
                if listing.count(x) == 0:
                    self._addChord(x, self._this_progression[int(x-x%1)], 'major')
                x += .25

    # This method adds notes to the measure which are off the beat.
    def _offbeat(self):
        for x in range(self._time[0]):
            # If there are enough notes to fill in the rest of the notes
            #   to be played, then play them all.
            if self._notes >= 4*(self._time[0]-x):
                self._addChord(x+.125, self._this_progression[x], 'major')
                self._addChord(x+.375, self._this_progression[x], 'major')
                self._addChord(x+.625, self._this_progression[x], 'major')
                self._addChord(x+.875, self._this_progression[x], 'major')
            else:
                chance = random.randrange(1 + self._notes*(100/self._complexity))
                if chance < self._notes:
                    self._addChord(x+.125, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes*(100/self._complexity))
                if chance < self._notes:
                    self._addChord(x+.375, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes*(100/self._complexity))
                if chance < self._notes:
                    self._addChord(x+.625, self._this_progression[x], 'major')
                chance = random.randrange(1 + self._notes*(100/self._complexity))
                if chance < self._notes:
                    self._addChord(x+.875, self._this_progression[x], 'major')
        

    # This method drops random notes from the measure based on the value
    #   of complexity.
    def _dropnotes(self):
        # Calculates the base number of drops. At full complexity, this should
        #   be 8 and should have a minimum of 0. The range from 1-8 is provided
        #   by dividing energy by 12. 
        drops = self._complexity/12
        # Modulates the number of drops based on the time signature. 
        drops = drops * self._time[0] / self._time[1]

        # If there were not many notes played (less then the number of onbeat
        #   notes available), then then number of drops should be limited
        if self._getNotes() < 4*self._time[0]:
            drops += self._getNotes() - 4*self._time[0]

        listing = self._plans.keys()
        # Iterate over all notes, and do it until all drops are used
        while drops > 0:
            for x in range(len(listing)):
                # If this note is divisible by a sixteenth note
                if (listing[x] % .25) == 0 and drops > 0:
                    # Randomly remove a note, where about 1 in every 4 should
                    #   be removed, until there are no more drops.
                    chance = random.randrange(4 * drops)
                    if chance < drops:
                        self._plans[listing[x]] = []
                        drops -= 1

# Returns the construtor for the AcousticGuitar		
def Musician():
    return AcousticGuitar()
