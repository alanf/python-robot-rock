
''' handdrum.py
    definition of a handdrum
    Author: Rich Snider <mrsoviet@cs.washington.edu
'''

from musicianStructured import MusicianStructured
import random


#incomplete HandDrum. Only plays quarter notes, should vary with time signature
#note: shoould fail testReactToChanges
class HandDrum(MusicianStructured):
    #Definition of a HandDrum

    def __init__(self, staff, energy=50, complexity=50):
        #Musician.__init__(staff, energy, complexity)
        self.id = 'handdrum'
        
        self.energy = energy
        self.complexity = complexity
        self.staff = staff
        #self.current_measure = self.staff.measures.next()
        self.current_measure = []
        #self.key =  self.current_measure.key
        #self.time =  self.current_measure.time_signature
        self.time = [4,4]
        self._plans = []
        self.changed = 1 #if a change is made, set changed to 1
                            #set to 0 by decide method when composing

    def _decide(self):
        #chooses if it needs to play new music
        #returns true when needs to compose new music
        if self.changed:
            changed = 0
            return True
        else:
            return False

    #assumes decide returned true
    #new music is generated
    def _write(self):
        #building a measure
        #possibly common to all musicians:
        self._plans = []
        notes = self.__getNotes()

        #specific to HandDrum
        self.__quarters(notes)
        #self.__eigths(notes)

    #find number of notes to play in the measure
    def __getNotes(self):
        #assumes 4/4 and 16 notes in a measure (1,e,&,a...)
        notes = self.energy/12
        notes = notes+(self.complexity/(100/notes))
        notes = notes * self.time[0] / self.time[1]
        #self.time[0] is 2, self.time[1] is 4 for 2/4 time
        return notes

    #fills in the main beats of the measure
    #if there are more notes to be played then beats, then all beats
    #   will have notes
    #if not, some beats will have notes, and no notes will be left for
    #   any other places in the measure (eigth notes, 16th notes, etc)
    def __quarters(self, notes): 

        #more, or equal, notes then beats, fill the beats
        if notes>=self.time[0]:
            self._plans.append(range(self.time[0]))
            notes-=self.time[0]

        #less notes then beats, need to fill some
        elif notes > 0: 
            #iterate over all of the beats in the measure
            for x in range(self.time[0]):
                #have enough notes to fill in remaining beats
                #so put a note on this beat
                if notes>=(self.time[0]-x):
                    self._plans.append(x)
                    notes-=1
                #not enough noted to fill in remaining beats
                #randomly choose if this beat will have a note
                else:
                    chance = random.randrange(self.time[0])
                    if chance < notes:
                        self._plans.append(x)
                        notes-=1


    #def __eigths(self, notes):
     #   fill = false
      #  if notes > self.time[0]:
       #     fill = true
        #for x in range(len(self._plans)):
            




