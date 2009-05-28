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
    
    def testCopy(self):
        self.score_slice.current_index = 5
        copy = self.score_slice.copy()
        
        self.assertEquals(self.score_slice.current_index, copy.current_index)
        
        # Ensure that changing the copy doesn't affect the original.
        copy.current_index = 123
        self.assertEquals(self.score_slice.current_index, 5)
        # Make sure that we are actually pointing to the staff data.
        self.assertEquals(copy[1][1], 'measure2')
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from scoreslice import ScoreSlice
    
    unittest.main()
            
        
