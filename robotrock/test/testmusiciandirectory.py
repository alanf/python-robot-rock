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
            acousticguitar=musicianmetadata.MusicianMetadata( \
	        'Acoustic Guitar', set(['acoustic','string']), None, ''), \
            electricguitar=musicianmetadata.MusicianMetadata( \
	        'Electric Guitar', set(['electric','string']), None, ''), \
            handdrum=musicianmetadata.MusicianMetadata( \
	        'Hand Drum', set(['percussion']), None, ''), \
            metronome=musicianmetadata.MusicianMetadata( \
	        'Metronome', set(['percussion']), None, ''))


    def testfilterMusicianList(self):
	''' Get the musician list for a variety of tag sets, and assert that
	    all the proper musicians are in the list based on their names
	'''
        music_list = self.musicDir.filterMusicianList(set(['acoustic']))
	name_list = [meta.name for meta in music_list]
        self.assertEqual(['Acoustic Guitar'], name_list)
	
        music_list = self.musicDir.filterMusicianList(set(['percussion']))
	name_list = [meta.name for meta in music_list]
        self.assertEqual(['Hand Drum', 'Metronome'], name_list)
	
        music_list = self.musicDir.filterMusicianList( \
	    set(['acoustic', 'percussion']))
	name_list = [meta.name for meta in music_list]
        self.assertEqual([], name_list)
	
        music_list = self.musicDir.filterMusicianList(set())
	name_list = [meta.name for meta in music_list]
        self.assertEqual(['Acoustic Guitar', 'Electric Guitar', 'Hand Drum', \
	    'Metronome',], name_list)
        
    def testvalidTags(self):
        tag_set = self.musicDir.validTags(set(['acoustic']))
        self.assertEqual(set(['string']), tag_set)
        tag_set = self.musicDir.validTags(set(['string']))
        self.assertEqual(set(['acoustic', 'electric']), tag_set)
        tag_set = self.musicDir.validTags(set(['percussion']))
        self.assertEqual(set([]), tag_set)
        tag_set = self.musicDir.validTags(set([]))
        self.assertEqual(set(['acoustic', 'electric', 'percussion', 'string']), \
	    tag_set)
        
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import musiciandirectory
    import musicianmetadata
    unittest.main()