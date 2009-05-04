#!/usr/bin/env python
''' conductor.py
    Author: Alan Fineberg (af@cs.washington.edu)
    The conductor is responsible for telling the AI to perform,
    and specifying their performance order.
    The onPulse() method is triggered for each metronome pulse.
'''
class Conductor(object):
    def __init__(self, ensemble):
        self.ensemble = []
        self.order = list(ensemble)
    
    # Add a musician to the ensemble, and place it
    # in the conductor's own internal musician order.
    def addMusician(self, musician):
        self.ensemble.append(musician)
        self.order.append(musician)
    
    # Remove the musician from the ensemble.
    # If the musician does not exist, the 
    # ValueError exception must be handled.
    def removeMusician(self, musician):
        self.ensemble.remove(musician)
        self.order.remove(musician)
    
    def onPulse(self, elapsed):
        for musician in self.order:
            musician.play(elapsed)

if __name__ == '__main__':
    conductor = Conductor(['musician1', 'musician2'])