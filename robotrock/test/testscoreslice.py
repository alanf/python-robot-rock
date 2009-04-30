#!/usr/bin/env python
''' testscoreslice.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Unit tests for ScoreSlice.
'''
import unittest
import sys

class TestScoreSlice(unittest.TestCase):
    def setUp(self):
        class StaffStub(object):
            def __init__(self, *measures):
                self.measures = measures
                
        staffs = [StaffStub('measure1', 'measure2', 'measure3', 'measure4'),
                  StaffStub('measure1', 'measure2', 'measure3', 'measure4'),
                  StaffStub('measure1', 'measure2', 'measure3', 'measure4')]
        self.score_slice = ScoreSlice(staffs)
        
        self.measure_labels = ['measure1', 'measure2', 'measure3', 'measure4']
        
    def testGetIndex(self):
        # Checks the result of all 4 score slices against the expected values.
        for (i, word) in enumerate(self.measure_labels):
            [self.assertEqual(word, result) for result in self.score_slice[i]]
        
    def testNext(self):
        for (i, word) in enumerate(self.measure_labels):
            [self.assertEqual(word, result) for result in self.score_slice.next()]
    
    def testPrevious(self):
        for (i, word) in enumerate(self.measure_labels):
            self.score_slice.next()
        
        # Move the cursor one more space, past the last item.
        self.score_slice.next()
        
        # Copy and reverse the list.
        reversed_labels = self.measure_labels[:]
        reversed_labels.reverse()
        
        for (i, word) in enumerate(reversed_labels):
            [self.assertEqual(word, result) for result in self.score_slice.previous()]
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from scoreslice import ScoreSlice
    
    unittest.main()
            
        
