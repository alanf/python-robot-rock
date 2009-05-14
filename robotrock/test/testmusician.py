#!/usr/bin/env python

''' testmusician.py
    Unit Tests for a musician
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
import unittest

class TestMusician(unittest.TestCase):

    #tests init settings
    def testInit(self):
        self.musician = MusicianStructured([])
        self.assertEqual(50, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)
        
        self.musician = MusicianStructured([], 40, 80)
        self.assertEqual(40, self.musician.energy)
        self.assertEqual(80, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)

        self.musician = MusicianStructured([], 42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)

    def testWrite(self):
        self.musician = MusicianStructured([], 42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)
    
        self.musician._write()
        self.assertNotEqual({}, self.musician._plans)

    def testGetAndSet(self):
        self.musician = MusicianStructured([])
        self.musician.energy = 23
        self.assertEqual(23, self.musician.energy)
        self.musician.complexity = 78
        self.assertEqual(78, self.musician.complexity)
        self.musician.time = [2,6]
        self.assertEqual([2,6], self.musician.time)
        self.musician.key = 'A'
        self.assertEqual('A', self.musician.key)
        
'''
    def testCompose(self):
        self.musician = MusicianStructured([], 42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(True, self.musician._changed)
    
        self.musician._compose()
        self.assertNotEqual({}, self.musician._plans)
'''
        

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from musicianStructured import MusicianStructured
    unittest.main()
