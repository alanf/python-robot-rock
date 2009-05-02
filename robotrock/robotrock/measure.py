#!/usr/bin/env python
''' measure.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Measure is a container for Notes, and also describes the current key and
    time signature, as well as other information necessary for playback of its
    notes.
'''
from expandinglist import ExpandingList
from note import Note

class Measure(object):
    def __init__(self, **measure_info):
        self.__dict__.update(measure_info)
        self.notes = ExpandingList(Note, self)

if __name__ == '__main__':
    measure = Measure(key=('C', '#', 'maj'), time=(4, 4), tempo=(120, 'bpm'))