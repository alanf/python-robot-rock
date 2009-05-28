#!/usr/bin/env python
# encoding: utf-8
'''
testbassmusician.py

Created by Alan Fineberg on 2009-05-26.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
'''
import unittest
import bassmusician
import unittest

class TestBassMusician(unittest.TestCase):
    def setUp(self):
        self.musician = bassmusician.Bass()
        class MeasureStub(object):
            def __init__(self):
                self.time_signature = (4, 4)
                self.key_signature = ('C', 'minor')
                self.notes = []
            def addNote(self, note):
                self.notes.append(note)
                
        self.measure = MeasureStub()
           
    def testCompose(self):
        self.musician._complexity = 100
        self.musician._energy = 100
        self.musician.compose(self.measure, 0, 1000, None)
        self.assertNotEqual(len(self.measure.notes), 0)

    
if __name__ == '__main__':
    unittest.main()