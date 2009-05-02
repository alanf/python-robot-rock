#!/usr/bin/env python
# encoding: utf-8
''' testmeasure.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Unit Tests for Measure.
'''

import sys
import unittest

class TestMeasure(unittest.TestCase):
    def setUp(self):
        pass
    
    def testCreateMeasure(self):
        measure = Measure(key=('C', '#', 'maj'), time=(4, 4), tempo=(120, 'bpm'))
        # Compare tuples using string comparison.
        self.assertEquals(str(measure.key), str(('C', '#', 'maj')))
        self.assertEquals(str(measure.tempo), str((120, 'bpm')))

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from measure import Measure
    unittest.main()