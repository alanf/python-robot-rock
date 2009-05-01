#!/usr/bin/env python
''' conductor.py
    Author: Alan Fineberg (af@cs.washington.edu)
    The conductor is responsible for telling the AI to perform.
    The onPulse() method is triggered for each metronome pulse.
'''
class Conductor(object):
    def __init__(self, ensemble):
        self.ensemble = ensemble
    
    def addMusician(self, musician):
        pass
    
    def removeMusician(self, musician):
        pass
    
    def onPulse(self, elapsed):
        for musician in self.ensemble:
            musician.compose('duration')

if __name__ == '__main__':
    conductor = Conductor(['musician1', 'musician2'])