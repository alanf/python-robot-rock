
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
        self.current_measure = self.staff.measures.next()
        self.key =  self.current_measure.key
        self.time =  self.current_measure.time_signature
        self.__plans = []
        self.changed = true
        self.__location = 0
        pass

    def play(self):
        #deciding if it needs to update plans        
        #writing to the score
        if self.__decide
            self.__compose
            #print __plans to measure

    #functions below are rewritten by individual musicians

    def __decide(self):   #private
        #chooses if it needs to play new music
        #returns true when needs to compose new music
        pass

    def __compose(self):  #private
        #new music is generated
        pass
