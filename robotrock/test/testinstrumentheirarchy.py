#!/usr/bin/env python
# encoding: utf-8
"""
testinstrumentheirarchy.py
Author: Alan Fineberg (af@cs.washington.edu)
Unit Tests for InstrumentHeirarchy
"""

import sys
import unittest


class TestInstrumentHeirarchy(unittest.TestCase):
    def setUp(self):
        self.instrument_heirarchy = InstrumentHeirarchy()
        self.instrument_data = \
                ['drum ||| percussion', 'guitar ||| string', 'bass ||| string', 'bass guitar ||| bass']
    
    def testLoadInstrumentData(self):
        self.instrument_heirarchy.loadInstrumentData(self.instrument_data)
    
    def testParent(self):
        self.instrument_heirarchy.loadInstrumentData(self.instrument_data)
        
        self.assertEquals(self.instrument_heirarchy.parent('drum'), 'percussion')
        self.assertEquals(self.instrument_heirarchy.parent('guitar'), 'string')
        self.assertEquals(self.instrument_heirarchy.parent('bass'), 'string')
        self.assertEquals(self.instrument_heirarchy.parent('bass guitar'), 'bass')
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from instrumentheirarchy import InstrumentHeirarchy
    unittest.main()