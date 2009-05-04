#!/usr/bin/env python

''' testmusician.py
    Unit Tests for a musician
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

import sys
import unittest

class TestMusician(unittesy.TestCase):

    def setup(self):
        return false

    def testInit(self):
        return false

    def testPlay(self):
        return false

    def testCompose(self):
        return false

    def testReactToChanges(self):
        return false

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    from musician import Musician
    unittest.main()
