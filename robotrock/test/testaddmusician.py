''' Integration test for adding a musician to the ensemble
    Author: Michael Beenen <beenen34@cs.washington.edu>
    
'''

import sys
import unittest

sys.path.append( "../robotrock")

import audiodriver
import conductor
import corecontroller
import atomicmetronome
import musicianstructured
import score
import songinfo



class TestAddMusician(unittest.TestCase):
    
    def setUp(self):
	# Set up all the necessary objects for using a core contorller and conductor
        self.metronome = atomicmetronome.AtomicMetronome()
        self.audio_driver = audiodriver.AudioDriver(self.metronome)
        self.score_object = score.Score()
        self.song_info = songinfo.SongInfo()
        self.conductor_object = conductor.Conductor(self.score_object, self.song_info)
        self.core_controller = corecontroller.CoreController(self.audio_driver, \
                self.metronome, self.conductor_object, self.song_info)

    def testaddMusician(self):
	# Ensure the ensemble starts as empty
	self.conductor_object.ensemble = []
	test_musician = musicianstructured.MusicianStructured()
	# Add test musician and ensure the conductors ensemble is updated accordingly
	self.core_controller.addMusician(test_musician)
	self.assertEquals(self.conductor_object.ensemble, [test_musician])
	
if __name__ == '__main__':
    unittest.main()



