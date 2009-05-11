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
        self.musicDir.musicians = dict(acoustic_guitar=frozenset(['acoustic', 'string']), \
                electric_guitar=frozenset(['electric', 'string']), \
                hand_drum=frozenset(['percussion']), \
                metronome=frozenset(['percussion']))


    def testfilterMusicianList(self):
        list = self.musicDir.filterMusicianList(frozenset(['acoustic']))
        self.assertEqual(['acoustic_guitar'], list)
        list = self.musicDir.filterMusicianList(frozenset(['percussion']))
        self.assertEqual(['hand_drum', 'metronome'], list)
        list = self.musicDir.filterMusicianList(frozenset(['acoustic', 'percussion']))
        self.assertEqual([], list)
        list = self.musicDir.filterMusicianList(frozenset())
        self.assertEqual(['acoustic_guitar', 'electric_guitar', 'hand_drum', \
                          'metronome'], list)
        
    def testvalidTags(self):
        list = self.musicDir.validTags(set(['acoustic']))
        self.assertEqual(['string'], list)
        list = self.musicDir.validTags(set(['string']))
        self.assertEqual(['acoustic', 'electric'], list)
        list = self.musicDir.validTags(set(['percussion']))
        self.assertEqual([], list)
        
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import musiciandirectory
    unittest.main()