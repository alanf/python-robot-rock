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

    # Initialization of a AcousticGuitar. Initializes AcousticGuitar2 specific
    #   values and leaves the rest to the super class __init__ method.
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        MusicianStructured.__init__(self, energy, complexity, time, key)
        self.instrument = 'acoustic guitar'
        self._my_tone= (key[0], 4)
        self._offnotes = 0
        self._last_progression = []
        self._this_progression = []
        self._last_index = 0
        self._this_index = self._time[0] - 3 # Starts 3 early for priming purposes

    # This method decides if new music needs to be composed on this iteration.
    def _decide(self):
        return self._changed

    # This method decides what will be played this iteration. This method
    #   assumes the whole measure needs to be rebuilt, so it does so.
    # For an AcousticGuitar2 this is done by playing a count of notes depending
    #   on energy and dropping notes depending on complexity.
    def _write(self):
        self._plans = {}
        self._progressions()
        self._notes = self._getNotes()
        self._locations()
        self._lengths()
        self._dynamics()
        self._changed = False

    # This method determines which chord progressions will be used for this measure
    # For simplicity, a given chord is played for a beat. Also, progressions are
    #   assumed to be 3 chords in length, hence the magic number 3 everywhere.
    #   To allow for varying progression lengths, simply replace the 3's with a
    #   variable holding the progression length.
    def _progressions(self):
        # Assume this is a new measure, as such, need to make room for this
        #   measure's progressions.
        # _last_progression is a list of the chords played in the last measure
        # _this_progression is a list of the chords to be played this measure
        #   _this_progression[0] is the chord played from beat 0 to beat 1
        #   _this_progression[1] is the chord played from beat 1 to beat 2, etc
        self._last_progression = self._this_progression
        self._this_progression = []
        # Indicies indicate the starts of of chord progressions. For simplicity,
        #   progressions are assumed to be 3 chords in length. Also, the last 
        #   index + 3 will always be >= the number of beats (self._time[0]).
        # The indicies are indicies into _last_progression and _this progression
        #   The chord at that index is the start of a chord progression. For
        #   simplicity, progressions are assumed to be 3 chords in length. Also,
        #   the last index + 3 will always be >= the number of beats
        #   (self._time[0]).
        self._last_index = self._this_index
        self._this_index = (self._this_index + 3) % self._time[0]
        
        # The first few chords in this measure are a continuation of a chord
        #   progression from the last measure, so start this measure with those
        #   chords. 
        if self._this_index > 0:
            # Get the presently playing progression (started in the last measure)
            listing = chords.Progressions[self._last_progression[self._last_index]]
            # Iterate over the remaining chords in the progression to be finished
            for x in range(3-self._this_index, 3):
                self._this_progression.append(listing[x])
                
        # Choose the chord progressions which will fill out the rest of this
        #   measure. Once one is chose, add it to _this_progression. If more
        #   chords need to be played, do it again.
        while self._this_index < self._time[0]:
            # At high complexity, the core progression should be played 1 of every
            #   4 progressions at minimum. At low complexity it should be the only
            #   progression played.
            chance = random.randrange(1+self._complexity/25)
            # A random progression is to be chosen (not going to play the core one)
            if chance > 0:
                # Randomly choose a progression (there are 17 major progressions)
                chance = random.randrange(17)
                prog = chords.Progressions.keys()[chance]
                self._this_progression.extend(chords.Progressions[prog])
            # Play the core progression
            else:
                self._this_progression.extend(chords.Progressions[self._key[0]])
            # Move the index forward by the length of the chord progression added
            self._this_index += 3

        # Set _this_index to be the start of the last progression played in this
        #   measure
        if self._this_index >= self._time[0]:
            self._this_index -= 3
        #self._this_index = self._time[0] - (3 - (self._this_index % self._time[0]))        

    # This method calculates the number of notes to be played in this
    #   measure. This calcluation is based on the energy and complexity
    #   presently set. The number of notes played varies with the time
    #   signature. energy and complexity range from 1 to 100 (or 0 to 99)
    # Just returns 4 for this version.
    def _getNotes(self):
        # Calculates the base number of notes. At full energy, this should
        #   be 4 and should have a minimum of 1. The 1 is provided by the
        #   leading 1 and the range from 1-4 is provided by dividing energy
        #   by 26. 
        notes = 1 + self._energy/26
        # Adds notes to the number of notes to be played due to complexity.
        #   The number of notes that are added is also a function of energy.
        #   More energy means more notes, and so does more complexity. But a
        #   high complexity and low energy shouldnt add too many notes. To
        #   do this, both energy and complexity need to be in the numerator;
        #   also, something needs to be in the denominator. 100 is found to be
        #   the correct denominator because complexity == 100, energy == 0, only
        #   one note is added. However, at complexity == 100, energy == 100, the
        #   number of notes is doubled.
        self._offnotes = (self._complexity/(100/notes))
        # Modulates the number of notes based on the time signature. 
        notes = notes * self._time[0] / self._time[1]
        self._offnotes = self._offnotes * self._time[0] / self._time[1]
        return notes

    # This method decides the start locations of all the notes in the to be
    #   played. It does this by splitting the job up into on-beat notes and
    #   off-beat notes. 
    def _locations(self):
        self._onbeat()
        self._notes = self._offnotes
        if self._notes > 0:
            self._offbeat()
            #self._dropnotes()
        

    # This method decides the length of each note in the measure. For a
    #   BassDrum, a note should run into the next note and be no more than
    #   a WHOLE_NOTE in length. 
    def _lengths(self):
        listing = self._plans.keys()
        listing.sort()

        for x in range(len(listing)):
            notelisting = self._plans[listing[x]]
            for y in range(len(notelisting)):
                if (x+1) < len(listing):
                    self._setLength(notelisting[y], listing[x+1] - listing[x])
                else:
                    self._setLength(notelisting[y], (self._time[0] + 1) - listing[x])


    # This method decides the dynamics of each note in the measure. Right now,
    #   everything is left to defualt (Forte).
    def _dynamics(self):
        pass

    # This method calculates the length of the given note based on the the given
    #   dist (distance) to the next note. The length of the note is made as
    #   long as possible without being longer than dist.
    def _setLength(self, myNote, dist):
        if dist >= 4.0:                     #whole note
            myNote.duration=self._durations.WHOLE_NOTE
        elif dist == 2.0:                   #half note
            myNote.duration=self._durations.HALF_NOTE
        elif dist >= 1.0:                   #quarter note
            myNote.duration=self._durations.QUARTER_NOTE
        elif dist == .5:                    #eighth note
            myNote.duration=self._durations.EIGHTH_NOTE
        elif dist == .25:                   #sixteenth note
            myNote.duration=self._durations.SIXTEENTH_NOTE
        elif dist == .125:                  #32'nd note
            myNote.duration=self._durations.THIRTYSECOND_NOTE
        elif dist == .0625:                 #64'th note
            myNote.duration=self._durations.SIXTYFOURTH_NOTE
        elif dist == .33:                   #tripolet   
            myNote.duration=self._durations.EIGHTH_NOTE_TRIPLET
        elif not(dist % .5):                #divisible by eigth note
            self._setLength(myNote, dist - .5)
        elif not(dist % .25):               #divisible by sixteenth note
            self._setLength(myNote, dist - .25)
        elif not(dist % .125):              #divisible by 32'nd note
            self._setLength(myNote, dist - .125)
        elif not(dist % .0625):             #divisible by 64'th note
            self._setLength(myNote, dist - .0625)
        elif not(dist % .33):               #divisible by tripolet
            self._setLength(myNote, dist - .33)
        else:#Somehow we fell through, default it to be as short as possible
            myNote.duration = self._durations.SIXTYFOURTH_NOTE

    # This method adds notes to the measure which are on the beat. 
    def _onbeat(self):
        # Iterate through all beats
        for x in range(self._time[0]):
            
            # If there are at least as many notes left to play as onbeat notes
            #   left to be played, then write all onbeat notes
            if self._notes >= (self._time[0]-x):
                self._addChord(x, (self._this_progression[x], 4), 'major')
                
            # If there are at least as many notes to play as half of the onbeat
            #   notes left to be played, then write at least half and randomly
            #   write the other onbeat notes
            elif self._notes >= (self._time[0]-x) / 2:
                # Put notes on odd beats (1,3,5,etc which are 0,2,4 etc in _plans)
                if not(x % 2):
                    self._addChord(x, (self._this_progression[x], 4), 'major')

        # There are still notes to be played that should be onbeat notes
        y = 0   # Prevents loop from going to long
        while self._notes > 0 and y < 20:
            listing = self._plans.keys()
            y += 1
            for x in range(self._time[0]):
                # There is no note here
                if listing.count(x) == 0:
                    # Randomly add a note here
                    chance = random.randrange(1 + self._notes * 2)
                    if chance < self._notes:
                        self._addChord(x, (self._this_progression[x], 4), 'major')

    # This method adds notes to the measure which are off the beat.
    def _offbeat(self):
        notes = self._notes
        # Iterate through all beats
        for x in range(self._time[0]):
            
            # There are enough notes to fill through sixteenth notes
            if self._notes >= 3*(self._time[0]-x):
                self._addChord(x+.25, (self._this_progression[x], 4), 'major')
                self._addChord(x+.5, (self._this_progression[x], 4), 'major')
                self._addChord(x+.75, (self._this_progression[x], 4), 'major')
                
            # There are enough notes to play all eighth notes
            elif self._notes >= (self._time[0]-x):
                self._addChord(x+.5, (self._this_progression[x], 4), 'major')

        # There are still offbeat notes left to be played
        y = 0   # Prevents loop from going to long
        while self._notes > 0 and y < 20:
            listing = self._plans.keys()
            y += 1
            for x in self._time[0]:
                # Randomly add notes
                chance = random.randrange(1 + self._notes * 4)
                if chance < self._notes and listing.count(x+.25) == 0:
                    self._addChord(x+.25, (self._this_progression[x], 4), 'major')
                chance = random.randrange(1 + self._notes * 2)
                if chance < self._notes and listing.count(x+.5) == 0:
                    self._addChord(x+.5, (self._this_progression[x], 4), 'major')
                chance = random.randrange(1 + self._notes * 4)
                if chance < self._notes and listing.count(x+.75) == 0:
                    self._addChord(x+.75, (self._this_progression[x], 4), 'major')        

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

# Returns the construtor for the AcousticGuitar2		
def Musician():
    return AcousticGuitar()
