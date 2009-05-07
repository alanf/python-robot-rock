
''' musician.py
    musician definition
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

class Musician(object):
    #Definition of what a Musician is

    def __init__(self, staff, energy=50, complexity=50):
        self.energy = energy
        self.complexity = complexity
        self.staff = staff
        #self.current_measure = self.staff.measures.next()
        self.current_measure = []
        #self.key =  self.current_measure.key
        #self.time =  self.current_measure.time_signature
        self.time = [4,4]
        self.__plans = []
        self.changed = 1 #if a change is made, set changed to 1
                            #set to 0 by decide method when composing
        
    def play(self): #called by conductor
        #deciding if it needs to update plans        
        #writing to the score
        if self.__decide():
            self.__compose()
        self.current_measure = self.__plans
            #print __plans to measure

    #functions below are rewritten by individual musicians

    def __decide(self):   #private
        #chooses if it needs to play new music
        #returns true when needs to compose new music
        return True

    def __compose(self):  #private
        #new music is generated
        for x in range(self.time[0]):
            self.__plans.append(x)
