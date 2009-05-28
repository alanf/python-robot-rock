#! usr/bin/env python

''' testcorecontrollor.py
    Author: Michael Beenen <beenen34@cs.washington.edu>
    Unit test for MusicianDirectory.
'''

import unittest
import sys

class AcousticGuitar(object):
    
    def __init__(self):
	pass

class ElectricGuitar(object):
    
    def __init__(self):
	pass
	
class HandDrum(object):
    
    def __init__(self):
	pass

class Metronome(object):
    
    def __init__(self):
	pass
	
	
def Musician(instrument):
    if instrument == 'acousticguitar':
        return AcousticGuitar
    if instrument == 'electricguitar':
        return ElectricGuitar
    if instrument == 'handdrum':
	return HandDrum
    if instrument == 'metronome':
	return Metronome
	
def trimMusicianList(list):
    new_list = []
    
    for i in list:
	new_list.append((i[0], i[1]))
	
    return new_list

class TestMusicianDirectory(unittest.TestCase):

    def setUp(self):
        self.musicDir = musiciandirectory.MusicianDirectory();
        self.musicDir.musicians = dict( \
	    acousticguitar=(set(['acoustic','string']), \
	    Musician('acousticguitar'), 'test.png'), \
            electricguitar=(set(['electric','string']), \
	    Musician('electricguitar'), 'test.png'), \
            handdrum=(set(['percussion']), Musician('handdrum'), 'test.png'), \
            metronome=(set(['percussion']), Musician('metronome'), 'test.png'))


    def testfilterMusicianList(self):
        list = trimMusicianList(self.musicDir.filterMusicianList(set(['acoustic'])))
        self.assertEqual([('acousticguitar', Musician('acousticguitar'))], list)
        list = trimMusicianList(self.musicDir.filterMusicianList \
	    (set(['percussion'])))
        self.assertEqual([('handdrum', Musician('handdrum')), \
	    ('metronome', Musician('metronome'))], list)
        list = trimMusicianList(self.musicDir.filterMusicianList \
	    (set(['acoustic', 'percussion'])))
        self.assertEqual([], list)
        list = trimMusicianList(self.musicDir.filterMusicianList(frozenset()))
        self.assertEqual([('acousticguitar', Musician('acousticguitar')), \
	    ('electricguitar', Musician('electricguitar')), \
	    ('handdrum', Musician('handdrum')),  \
            ('metronome', Musician('metronome'))], list)
        
    def testvalidTags(self):
        list = self.musicDir.validTags(set(['acoustic']))
        self.assertEqual(['string'], list)
        list = self.musicDir.validTags(set(['string']))
        self.assertEqual(['acoustic', 'electric'], list)
        list = self.musicDir.validTags(set(['percussion']))
        self.assertEqual([], list)
	list = self.musicDir.validTags(set([]))
	self.assertEqual(['acoustic', 'electric', 'percussion', 'string'], list)
        
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import musiciandirectory
    unittest.main()