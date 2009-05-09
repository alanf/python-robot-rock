#!/usr/bin/env python
''' songinfo.py
    Module designed to store information about the style of the music.
    Contains information about the key and time signature
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

class SongInfo(object):
    def __init__(self):
	self.info = {
	             'key_signature': ('C', 'Natural', 'Major'),
	             'time_signature': (4, 4),
		    }
		     
    
    # Returns a copy of the current song info
    def measureInfo(self):
	measure_info = dict(self.info)
	return measure_info
