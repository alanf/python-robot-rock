#!/usr/bin/env python
''' testscore.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Unit Tests for Score.
'''
import unittest
import hihat


class TestHiHat(unittest.TestCase):
    def testCreateHiHat(self):
        m = hihat.Musician()
        self.assertEquals(m.__class__.__name__, 'HiHat')
        
if __name__ == '__main__':
    unittest.main()