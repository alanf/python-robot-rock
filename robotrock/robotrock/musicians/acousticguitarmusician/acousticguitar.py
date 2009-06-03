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
import tone

# This is the definition of an acoustic guitar
class AcousticGuitar(MusicianStructured):
    '''
    #listening: measure.parent.instrument
    #current_score_slice is a list of measures'''

    # Initialization of a AcousticGuitar. Initializes AcousticGuitar specific
    #   values and leaves the rest to the super class __init__ method.
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        MusicianStructured.__init__(self, energy, complexity, time, key)
        self.instrument = 'acoustic guitar'
        self._my_tone= (key[0], 4)
        self._offnotes = 0
        self._progression = []
        self._index = 0
        self._length = self._time[0]

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

    # This method determines which chord progressions will be used for this measure
    # For simplicity, a given chord is played for a beat. Also, progressions are
    #   assumed to be 3 chords in length, hence the magic number 3 everywhere.
    #   To allow for varying progression lengths, simply replace the 3's with a
    #   variable holding the progression length.
    def _progressions(self):
        if self._index >= self._time[0]:
            for x in range(self._time[0]):
                self._progression.pop(0)
            self._index -= self._time[0]
        progression = self._chooseProgression()
        while self._index < self._time[0]:
            self._setLen()
            for x in range(self._length):
                self._progression.append(progression[0])
                self._index+=1
            for x in range(self._length):
                self._progression.append(progression[1])
                self._index+=1
            for x in range(self._length):
                self._progression.append(progression[2])
                self._index+=1

    # Determines and returns the next chord progression to be played.
    def _chooseProgression(self):
        startChord = self._key[0]

        if random.randrange(1+self._complexity/25):
            chance = random.randrange(11)
            startChord = tone.getTone((startChord,4), chance)[0]
            
        result = [startChord]
        result.append(tone.getTone((startChord,4), tone.SUBDOMINANT)[0])
        result.append(tone.getTone((startChord,4), tone.DOMINANT)[0])
        return result

    # TDetermines the length of each chord in the measure (how many beats it is played).
    def _setLen(self):
        if self._complexity > 60:
            self._length = random.randint(1, self._time[0])
        elif self._complexity > 30:
            self._length = random.randint(self._time[0]/2, self._time[0]+self._time[0]/2)
        else:
            self._length = random.randint(self._time[0], self._time[0]*2)

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
                self._addChord(x, (self._progression[x], 4), self._key[1])
                
            # If there are at least as many notes to play as half of the onbeat
            #   notes left to be played, then write at least half and randomly
            #   write the other onbeat notes
            elif self._notes >= (self._time[0]-x) / 2:
                # Put notes on odd beats (1,3,5,etc which are 0,2,4 etc in _plans)
                if not(x % 2):
                    self._addChord(x, (self._progression[x], 4), self._key[1])

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
                        self._addChord(x, (self._progression[x], 4), self._key[1])

    # This method adds notes to the measure which are off the beat.
    def _offbeat(self):
        notes = self._notes
        # Iterate through all beats
        for x in range(self._time[0]):
            
            # There are enough notes to fill through sixteenth notes
            if self._notes >= 3*(self._time[0]-x):
                self._addChord(x+.25, (self._progression[x], 4), self._key[1])
                self._addChord(x+.5, (self._progression[x], 4), self._key[1])
                self._addChord(x+.75, (self._progression[x], 4), self._key[1])
                
            # There are enough notes to play all eighth notes
            elif self._notes >= (self._time[0]-x):
                self._addChord(x+.5, (self._progression[x], 4), self._key[1])

        # There are still offbeat notes left to be played
        y = 0   # Prevents loop from going to long
        while self._notes > 0 and y < 20:
            listing = self._plans.keys()
            y += 1
            for x in self._time[0]:
                # Randomly add notes
                chance = random.randrange(1 + self._notes * 4)
                if chance < self._notes and listing.count(x+.25) == 0:
                    self._addChord(x+.25, (self._progression[x], 4), self._key[1])
                chance = random.randrange(1 + self._notes * 2)
                if chance < self._notes and listing.count(x+.5) == 0:
                    self._addChord(x+.5, (self._progression[x], 4), self._key[1])
                chance = random.randrange(1 + self._notes * 4)
                if chance < self._notes and listing.count(x+.75) == 0:
                    self._addChord(x+.75, (self._progression[x], 4), self._key[1])        

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
