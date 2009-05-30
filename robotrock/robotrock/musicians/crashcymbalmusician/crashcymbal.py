''' crashcymbal.py
    definition of a crashcymbal
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
import random
sys.path.append('../shared')
from musicianstructured import MusicianStructured
sys.path.append('../..')
import note
import dynamics
from drumkit import DrumKit

# This is the definition of a CrashCymbal
class CrashCymbal(MusicianStructured):

    # Initialization of a CrashCymbal. Initializes CrashCymbal specific values and
    #   leaves the rest to the super class __init__ method.
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        MusicianStructured.__init__(self, energy, complexity, time, key)
        self.instrument = 'crash cymbal'
        self._my_tone=DrumKit["crash cymbal 1"]

    # This method decides if new music needs to be composed on this iteration.
    def _decide(self):
        # Needs to generate new music if something has changed
        return self._changed

    # This method decides what will be played this iteration. This method
    #   assumes the whole measure needs to be rebuilt, so it does so.
    # For a CrashCymbal, this is done by playing mainly on-beat notes (as able)
    #   and filling in with random off-beat notes as allowed by complexity.
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
        #   also, something needs to be in the denominator. 200 is found to be
        #   the correct denominator because complexity == 100, energy == 0, only
        #   one note is added. However, at complexity == 100, energy == 100, the
        #   number of notes increases by half as much.
        self._offnotes = (self._complexity/(200/notes))
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

    # This method decides the length of each note in the measure. For a
    #   CrashCymbal, a note should run into the next note and be no more than
    #   a QUARTER_NOTE in length. 
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
        if dist >= 1.0:                     #quarter note
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
        elif dist == 0:                     #Base case
            myNote.duration = self._durations.QUARTER_NOTE
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
                self._addNote(x, self._my_tone)
                
            # If there are at least as many notes to play as half of the onbeat
            #   notes left to be played, then write at least half and randomly
            #   write the other onbeat notes
            elif self._notes >= (self._time[0]-x) / 2:
                # Put notes on odd beats (1,3,5,etc which are 0,2,4 etc in _plans)
                if not(x % 2):
                    self._addNote(x, self._my_tone)

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
                        self._addNote(x, self._my_tone)   

    # This method adds notes to the measure which are off the beat.
    def _offbeat(self):
        listing = self._plans.keys()
        y = 0
        # Do it until all notes are added, or hae done it too many times
        while self._notes > 0 and y < 20:
            y += 1
            # Randomly add lagging eighths
            for x in range(self._time[0]):
                # There are notes left and this is a beat, so give it a chance.
                if self._notes > 0 and listing.count(x):
                    chance = random.randrange(1 + self._notes * 2)
                    if chance < self._notes:
                        self._addNote(x+.5, self._my_tone) 

            # Randomly add leading eighths
            for x in range(self._time[0]):
                # There are notes left, this is a beat, and it is not beat 0,
                #   so give it a chance. Needs to not be beat 0 because leading
                #   notes are being added.
                if self._notes > 0 and listing.count(x) and x:
                    chance = random.randrange(1 + self._notes * 4)
                    if chance < self._notes:
                        self._addNote(x-.5, self._my_tone)
                        
# Returns the construtor for the CrashCymbal		
def Musician():
    return CrashCymbal()
