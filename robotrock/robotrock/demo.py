#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Alan Fineberg on 2009-05-03.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from score import Score
from staff import Staff
from conductor import Conductor
from demoparser import SimpleParser
import note

from metronomemusician import MetronomeMusician

def main():
    # Create a score.
    score = Score()

    # Create a musician.
    musician = MetronomeMusician()
    # Establish that the NEXT measure created is 4/4 time.

    class SyncopatedMetronome(object):
        def __init__(self):
            self.instrument = 'syncopated metronome'
            self.__duration_map = {'quarter': 1}
            self.counter = 0
            
        def compose(self, measure, duration):
            if self.counter % 4 == 1 or self.counter % 4 == 3:
                myNote = note.Note(tone=38, duration='quarter', rest=False)
            else: # play a rest
                myNote = note.Note(tone=0, duration='quarter', rest=True)
            
            self.counter += 1
            measure.notes.append(myNote)
            
    # Stubbed
    class SongInfo(object):
        def measureInfo(self):
            return dict(key=('C', 'natural', 'major'), \
                        time_signature=(4, 4))

    # Create a conductor.
    conductor = Conductor(score, SongInfo())
    conductor.addMusician(musician)
    conductor.addMusician(SyncopatedMetronome())
    conductor.chunks_per_beat = 1
    
    # Create a parser.
    import fluidsynth
    synth = fluidsynth.Synth()
    synth.start()
    id = synth.sfload("HS_R8_Drums.sf2")
    synth.program_select(0, id, 0, 0)
    synth.sfont_select(0, id)
    parser = SimpleParser(score, synth)
    
    # Play ball!
    from time import time
    from time import sleep
    
    conductor.onPulse('tick')
    # Here, the conductor and the parser have the same resolution.
    for i in xrange(1000):
        print 'tick'
        parser.onPulse('tick')
        conductor.onPulse('tick')
        sleep(.250)

if __name__ == '__main__':
    main()

