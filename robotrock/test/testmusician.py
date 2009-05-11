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
        self.assertEqual([], self.musician.staff)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(1, self.musician.changed)
        
        self.musician = MusicianStructured([], 40, 80)
        self.assertEqual(40, self.musician.energy)
        self.assertEqual(80, self.musician.complexity)
        self.assertEqual([], self.musician.staff)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(1, self.musician.changed)

        self.musician = MusicianStructured([], 42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([], self.musician.staff)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(1, self.musician.changed)

    def testCompose(self):
        self.musician = MusicianStructured([], 42)
        self.assertEqual(42, self.musician.energy)
        self.assertEqual(50, self.musician.complexity)
        self.assertEqual([], self.musician.staff)
        self.assertEqual([4,4], self.musician.time)
        self.assertEqual(1, self.musician.changed)
    
        self.musician.compose()
        self.assertNotEqual([], self.musician.current_measure)
        #self.musician.play()
        #self.assertNotEqual([], getCurrentMeasure(musician))
        

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from musicianStructured import MusicianStructured
    unittest.main()
