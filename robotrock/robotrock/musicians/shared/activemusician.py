#!/usr/bin/env python
# encoding: utf-8
"""
activemusician.py

Created by Alan Fineberg on 2009-05-03.
"""
import sys
sys.path.append('../..')
import note
import dynamics
import drumkit

class ActiveMusician(object):
    def __init__(self):
        self._energy = 50
        self._complexity = 50
        self.changed = False
    
    def compose(self, measure, window_start, window_duration):
        pass

    def __setComplexity(self, value):
        self._complexity = value
        self.changed = True
    
    def __setEnergy(self, value):
        self._energy = value
        self.changed = True
    
    complexity = property(fset=__setComplexity)
    energy = property(fset=__setEnergy)

