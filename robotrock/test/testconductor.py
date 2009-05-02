#!/usr/bin/env python
''' testconductor.py
    Unit Tests for Conductor class.
    Author: Alan Fineberg (af@cs.washington.edu)
'''
import sys
import unittest

class TestConductor(unittest.TestCase):
    def setUp(self):
        self.test_log = []
        
        class Musician(object):
            def __init__(self, id, log):
                self.id = id
                self.log = log
            
            def compose(self, duration):
                self.log.append(self.id)
        
        self.musicians = [Musician(i, self.test_log) for i in range(0, 10)]
        self.conductor = Conductor(self.musicians)
    
    def testCompose(self):
        self.conductor.onPulse('some_value')
        [self.assertEqual(i, log_item) for (i, log_item) in \
                enumerate(self.test_log)]
    
    def testAddMusician(self):
        m = ['stub musician object']
        self.conductor.addMusician(m)
        self.assertTrue(m in self.conductor.ensemble)
        self.assertTrue(m in self.conductor.order)
    
    def testRemoveMusician(self):
        m = self.musicians[5]
        self.conductor.removeMusician(m)
        self.assertFalse(m in self.conductor.ensemble)
        self.assertFalse(m in self.conductor.order)
    
    def testConductorFollowsOrder(self):
        self.conductor.order = reversed(self.musicians)
        [self.assertEqual(i, log_item) for (i, log_item) in \
                enumerate(reversed(self.test_log))]

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from conductor import Conductor
    unittest.main()
