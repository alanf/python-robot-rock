#! usr/bin/env python

''' testcorecontrollor.py
    Author: Michael Beenen <beenen34@cs.washington.edu>
    Unit test for MusicianDirectory.
'''

import unittest
import sys

class TestMusicianDirectory(unittest.TestCase):

    def setUp(self):
        self.musicDir = musiciandirectory.MusicianDirectory();

    def testfilterMusicianList(self):
        list = self.musicDir.filterMusicianList(frozenset(['acoustic']))
        self.assertEqual(['acoustic_guitar'], list)
        list = self.musicDir.filterMusicianList(frozenset(['percussion']))
        self.assertEqual(['hand_drum', 'metronome'], list)
        
    def testvalidTags(self):
        list = MusicianDirectory.valid_tags(['acoustic'])
        self.assertEqual(['string'], list)
        list = MusicianDirectory.valid_tags(['string'])
        self.assertEqual(['acoustic', 'electric'], list)
        
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import musiciandirectory
    unittest.main()