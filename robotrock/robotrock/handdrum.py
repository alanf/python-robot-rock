''' handdrum.py
    TODO: Full explanation of handdrum class definition of a handdrum
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

from drumkit import DrumKit
import dynamics
from musicianstructured import MusicianStructured
import random
import note


# I prefer comments that are complete sentences, and that start with a space.
#incomplete HandDrum. Only plays quarter notes, should vary with time signature
#note: should fail testReactToChanges
class HandDrum(MusicianStructured):

    # TODO: I'm a fan of full sentence comments.
    #initialize the handdrum musician
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        MusicianStructured.__init__(self, energy, complexity, time, key)
        self.instrument = 'handdrum'
        self._my_tone=DrumKit["High Tom"]

    #decides if new music needs to be generated.
    #returns true when new music is to be generated
    #returns false otherwise
    def _decide(self):
        #needs to generate new music if something changed
        return self._changed

    #fills in a measure by writing to _plans
    #_plans is the temporary storage for all notes, they are printed
    #   to the measure after the notes have been fully determined
    #assumes that the whole measure needs to be rebuilt. as a result,
    #   the last version of the measure is essentially deleted
    def _write(self):
        self._plans = {}
        self._notes = self._getNotes()
        self._locations()
        self._lengths()
        self._dynamics()
        self._changed = False

    #find number of notes to play in the measure
    def _getNotes(self):
        #assumes 4/4 and 16 notes in a measure (1,e,&,a...)
        # TODO: Magic number 13 -> needs a variable name and comments
        notes = 1 + self._energy/13
        # Also here: document what 100 is.
        notes = notes+(self._complexity/(100/notes))
        notes = notes * self._time[0] / self._time[1]
        #self.time[0] is 2, self.time[1] is 4 for 2/4 time
        return notes

    #determines where all of the notes will be for this measure
    #notes is the number of notes there are to work with
    def _locations(self):
        self._onbeat()
        self._offbeat()

    #determines the lengths of each of the notes
    #this version is for drums only, makes the notes as long as possible
    #   up to a quarter note so that it fits without overlapping any other
    #   note
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


    #determines the dynamics of each note
    #this version sets all values to be middle of the road (50)    
    def _dynamics(self):
        pass

    #works for _lengths by setting the lengths themselves
    #myNote is the note being edited at the moment
    #diff is the space in time from the start of this note to the start
    #   of the next note
    def _setLength(self, myNote, diff):
        if diff >= 1.0:                     #quarter note
            myNote.duration=self._durations.QUARTER_NOTE
        elif diff == .5:                    #eigth note
            myNote.duration=self._durations.EIGHTH_NOTE
        elif diff == .25:                   #sixteenth note
            myNote.duration=self._durations.SIXTEENTH_NOTE
        elif diff == .125:                  #32'nd note
            myNote.duration=self._durations.THIRTYSECOND_NOTE
        elif diff == .0625:                 #64'th note
            myNote.duration=self._durations.SIXTYFOURTH_NOTE
        elif diff == .33:                   #tripolet   
            myNote.duration=self._durations.EIGHTH_NOTE_TRIPLET
        elif not(diff % .5):                #divisible by eigth note
            self._setLength(myNote, diff - .5)
        elif not(diff % .25):               #divisible by sixteenth note
            self._setLength(myNote, diff - .25)
        elif not(diff % .125):              #divisible by 32'nd note
            self._setLength(myNote, diff - .125)
        elif not(diff % .0625):             #divisible by 64'th note
            self._setLength(myNote, diff - .0625)
        elif not(diff % .33):               #divisible by tripolet
            self._setLength(myNote, diff - .33)
        else:#somehow we fell through, default it to be as short as possible
            myNote.duration = self._durations.SIXTYFOURTH_NOTE

    #determines where all of the on beat notes are
    #notes is the number of notes still availible
    #this version fills in all of the on beat notes before filling in
    #   off beat notes
    def _onbeat(self):

        #there are more notes left to play than there are beats
        if self._notes>=self._time[0]:
            for x in range(self._time[0]):
                self._addNote(x, self._my_tone)

        #less notes then beats, need to fill some
        elif self._notes > 0: 
            #iterate over all of the beats in the measure
            for x in range(self._time[0]):
                if self._notes > 0: 
                    #have enough notes to fill in remaining beats
                    #so put a note on this beat
                    if self._notes>=(self._time[0]-x):
                        self._addNote(x, self._my_tone)
                    #not enough noted to fill in remaining beats
                    #randomly choose if this beat will have a note
                    else:
                        chance = random.randrange(self._time[0])
                        if chance < self._notes:
                            self._addNote(x, self._my_tone)            

    #determines where all off beat notes are located
    #notes is the number of notes still availible
    def _offbeat(self):
        # TODO: update these comments
        #case1: just a few left (less than the number spaces for eighth notes)
        #case2: some notes (more than eighth spaces, less than 16th
        #case3: lots of notes (enough to fill 16th)
        #case4: more notes (more notes than through 16th notes) (not implemented)

        #case: lots of notes
        #3 beacuse 1/4 have been written (quarters)
        if self._notes >= (3*self._time[0]):
            #fill in 16th notes
            for x in range(self._time[0]):
                self._addNote(x+.25, self._my_tone)
                self._addNote(x+.5, self._my_tone)
                self._addNote(x+.75, self._my_tone)

        #case: some notes
        #there are enough notes to play all eighth notes, so lets play some.
        #   we also need to add some 16th notes
        elif self._notes > 0:
            #sixteenth notes
            for x in range(self._time[0]):
                #have enough notes to fill in remaining sixteenth notes
                if 0 < self._notes>=(self._time[0]-x):
                    # TODO: cleanup magic numbers 
                    self._addNote(x+.25, self._my_tone)
                    self._addNote(x+.5, self._my_tone)
                    self._addNote(x+.75, self._my_tone)
                #not enough notes to fill in remaining sixteenth notes
                #randomly choose if this beat will have some sixteenth notes
                else:
                    chance = random.randrange(2*self._time[0])
                    if chance < self._notes:
                        self._addNote(x+.25, self._my_tone)
                    chance = random.randrange(2*self._time[0])
                    if chance < self._notes:
                        self._addNote(x+.5, self._my_tone)
                    chance = random.randrange(2*self._time[0])
                    if chance < self._notes:
                        self._addNote(x+.75, self._my_tone)
			
def Musician():
    HandDrum()
