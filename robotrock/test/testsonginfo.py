#!/usr/bin/env python
'''testsonginfo.py
   Unit test for SongInfo
   Author: Michael Beenen <beenen34@cs.washington.edu>
'''

import sys
import unittest

class TestSongInfo(unittest.TestCase):
    def setUp(self):
	self.song_info = songinfo.SongInfo()
	self.dict = {
	             'key_signature': ('C', 'Natural', 'Major'),
		     'time_signature': (4, 4),
	            }
	
    def testmeasureInfo(self):
	self.assertEqual(self.song_info.measureInfo(), self.song_info.info)
	info_dict = self.song_info.measureInfo()
	self.song_info.info['time_signature'] = (2, 4)
	self.assertEqual(self.dict, info_dict)
	self.song_info.info['key_signature'] = ('D', 'Sharp', 'Minor')
	self.assertEqual(self.song_info.measureInfo(), self.song_info.info)
	
	
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import songinfo
    unittest.main()
	       
