#!/usr/bin/env python
# encoding: utf-8
"""
instrumentheirarchy.py
Author: Alan Fineberg (af@cs.washington.edu)
InstrumentHeirarchy is a class used to load and report instrument family classifcations.
"""

class InstrumentHeirarchy(object):
    def __init__(self):
        self.instruments = {}
    
    def loadInstrumentData(self, instrument_file):
        for line in instrument_file:
            (instrument, parent) = line.split('|||')
            self.instruments[instrument.strip()] = parent.strip()
            
    def parent(self, instrument):
        return self.instruments[instrument]

if __name__ == '__main__':
	instrument_heirarchy = InstrumentHeirarchy()

