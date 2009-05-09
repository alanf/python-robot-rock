#!/usr/bin/env python
''' testscore.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Unit Tests for Score.
'''
import unittest
import sys


class TestScore(unittest.TestCase):
    def testCreateScore(self):
        score = Score()
        self.assertNotEquals(score.staffs[0], None)
        self.assertNotEquals(score.score_slices, None)
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from score import Score
        
    unittest.main()