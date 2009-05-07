#! usr/bin/env python

''' testcorecontrollor.py
    Author: Michael Beenen <beenen34@cs.washington.edu>
    Unit test for MusicianDirectory.
'''

import unittest
import sys

class TestMusicianDirectory(unittest.TestCase):

    def testfilter_musician_list(self):
        list = MusicianDirectory.filter_musician_list(['acoustic'])
        self.assertEqual(['acoustic guitar'], list)
        list = MusicianDirectory.filter_musician_list(['percussion'])
        self.assertEqual(['hand drum'], list)
        
    def testvalid_tags(self):
        list = MusicianDirectory.valid_tags(['acoustic'])
        self.assertEqual(['string'], list)
        list = MusicianDirectory.valid_tags(['string'])
        self.assertEqual(['acoustic', 'electric'], list)
        
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import musiciandirectory
    unittest.main()