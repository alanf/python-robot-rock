#!/usr/bin/env python
''' testexpandinglist.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Unit tests for Expanding List.
'''
import unittest
import sys

class Stub(object):
    def __init__(self, **args):
        self.__dict__.update(args)
                
class TestExpandingList(unittest.TestCase):     
    def setUp(self):
        self.expanding_list = ExpandingList(Stub, id=23)
        
    def testExpand(self):
        self.assertEqual(self.expanding_list[6].id, 23)
        self.assertEqual(len(self.expanding_list), 7)
    
    def testNext(self):
        for i in xrange(100):
            self.expanding_list.append(Stub(id=i))
        
        previous = -1
        for i in xrange(100):
            id = self.expanding_list.next().id
            self.assertEquals(id - previous, 1)
            previous = id
        
    def testPrevious(self):
        # Fill the list with sequential values using list syntax.
        self.expanding_list = ExpandingList(Stub)
        for i in xrange(100):
            self.expanding_list.append(Stub(id=i))
        
        for i in xrange(10):
            self.expanding_list.next()
        
        # One more to move the cursor past the end of the list.
        self.expanding_list.next()
        
        for i in xrange(10, 0, -1):
            stub = self.expanding_list.previous()
            self.assertEquals(i - 1, stub.id)
    
    def testPreviousEdgeCase(self):
        self.assertEqual(self.expanding_list.previous(), None)
    
    def testPreviousEdgeCaseReset(self):
        self.expanding_list = ExpandingList(Stub, id=7)
        self.expanding_list.append(Stub(id=7))

        self.assertEqual(self.expanding_list.previous(), None)
        self.assertEqual(self.expanding_list.next().id, 7)
        self.assertEqual(len(self.expanding_list), 1)
            
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from expandinglist import ExpandingList
    
    unittest.main()