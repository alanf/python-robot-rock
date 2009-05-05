
''' handdrum.py
    definition of a handdrum
    Author: Rich Snider <mrsoviet@cs.washington.edu
'''

from musician import Musician
import random

class HandDrum(Musician):
    #Definition of a HandDrum

    def __init__(self, staff, energy=50, complexity=50):
        super.__init__(staff, energy, complexity)
        self.id = handdrum

    def __decide(self):
        #chooses if it needs to play new music
        #returns true when needs to compose new music
        if self.changed:
            return true
        else:
            return false

    def __compose(self):
        #assumes decide returned true
        #new music is generated

        #build a measure
        
        old = self.plans
        self.__plans = []

        #find number of notes to play in the measure
        #assumes 4/4 and 16 notes in a measure (1,e,&,a...)
        notes = self.energy/12
        notes = notes+(self.complexity/(100/notes))
        notes = notes * self.time[0] / self.time[1]
        #self.time[0] is 2, self.time[1] is 4 for 2/4 time

        quarters(notes)
        #eigths(notes)

        

    #fills in the main beats of the measure
    #if there are more notes to be played then beats, then all beats
    #   will have notes
    #if not, some beats will have notes, and no notes will be left for
    #   any other places in the measure (eigth notes, 16th notes, etc)
    def quarters(self, notes): 

        #more, or equal, notes then beats, fill the beats
        if notes>=self.time[0]:
            self.__plans.append(range(self.time[0]))
            notes-=range(self.time[0])

        #less notes then beats, need to fill some
        elif notes > 0: 
            #iterate over all of the beats in the measure
            for x in range(self.time[0]):
                #have enough notes to fill in remaining beats
                #so put a note on this beat
                if notes>=(self.time[0]-x):
                    self.plans.append(x)
                    notes-=1
                #not enough noted to fill in remaining beats
                #randomly choose if this beat will have a note
                else:
                    chance = random.randrange(self.time[0])
                    if chance < notes:
                        self.__plans.append(x)
                        notes-=1


    #def eigths(self, notes):
     #   fill = false
      #  if notes > self.time[0]:
       #     fill = true
        #for x in range(len(self.__plans)):
            




