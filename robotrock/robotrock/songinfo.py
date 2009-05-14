#!/usr/bin/env python
''' songinfo.py
    Module designed to store information about the style of the music.
    Contains information about the key and time signature
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

VALID_KEY = set(['A','A#','Ab','B','B#','Bb','C','C#','Cb',\
        'D','D#','Db','E', 'E#','Eb','F','F#','Fb','G','G#','Gb' ])
VALID_KEY_TONALITIES = set(['Major', 'Minor'])

VALID_TIME_NUMERATOR = set([2, 3, 4, 5, 6, 7])
VALID_TIME_DENOMINATOR = set([2, 4, 8])

class SongInfo(object):
    def __init__(self):
        self.info = {
                     'key_signature': ('C', 'Major'),
                     'time_signature': (4, 4),
                    }
                     
    
    # Returns a copy of the current song info
    def measureInfo(self):
        measure_info = dict(self.info)
        return measure_info
