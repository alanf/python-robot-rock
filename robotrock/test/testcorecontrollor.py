#! usr/bin/env python

''' testcorecontrollor.py
    Author: Michael Beenen <beenen34@cs.washington.edu>
    Unit test for CoreControllor.
'''
import unittest
import sys

class TestCoreController(unittest.TestCase):
    def setUp(self):
        
        # Stub class for Metronome 
        class Metronome(object):
            
            def __init__(self):
                self.tempo = 60
            
            def setTempo(self,tempo):
                self.tempo = tempo
        
        # Stub class for AudioDriver
        class AudioDriver(object):
            
            def __init__(self):
                self.playing = False
            
            def play(self):
                self.playing = True
            
            def pause(self):
                self.playing = False
            
            def isPlaying(self):
                return self.playing
        
        # Stub class for Conductor
        class Conductor(object):
            
            def __init__(self):
                self.ensemble = []
                
            def addMusician(self, musician):
                self.ensemble.append(musician)
            
            def removeMusician(self, musician):
                self.ensemble.remove(musician)
        
        self.metronome = Metronome()
        self.audio_driver = AudioDriver()
        self.song_info = songinfo.SongInfo()
        self.conductor = Conductor()
        self.corecontroller = corecontroller.CoreController(self.audio_driver, \
                self.metronome, self.conductor, self.song_info)
                
        self.corecontroller.music_dir.musicians = dict(
                acoustic_guitar=frozenset(['acoustic', 'string']), \
                electric_guitar=frozenset(['electric', 'string']), \
                hand_drum=frozenset(['percussion']), \
                metronome=frozenset(['percussion']))
    
    def testplay(self):
        self.corecontroller.play()
        self.assertTrue(self.audio_driver.isPlaying())
    
    def testpause(self):
        self.corecontroller.play()
        self.corecontroller.pause()
        self.assertFalse(self.audio_driver.isPlaying())
    
    def testsetTempo(self):
        self.corecontroller.setTempo(120)
        self.assertEqual(self.metronome.tempo, 120)
        self.corecontroller.setTempo(0)
        self.assertEqual(self.metronome.tempo, 0)
        self.corecontroller.setTempo(93)
        self.assertEqual(self.metronome.tempo, 93)
        self.corecontroller.setTempo(40)
        self.assertEqual(self.metronome.tempo, 40)
        self.corecontroller.setTempo(210)
        self.assertEqual(self.metronome.tempo, 210)
        self.corecontroller.setTempo(215)
        self.assertEqual(self.metronome.tempo, 215)
    
    def testupdateTimeSignature(self):
        self.corecontroller.updateTimeSignature((3, 4))
        info = self.corecontroller.song_info.measureInfo()
        self.assertEqual(info['time_signature'], (3, 4))
        self.corecontroller.updateTimeSignature((2, 4))
        info = self.corecontroller.song_info.measureInfo()
        self.assertEqual(info['time_signature'], (2, 4))
        self.corecontroller.updateTimeSignature((0, 2))
        info = self.corecontroller.song_info.measureInfo()
        self.assertEqual(info['time_signature'], (2, 4))
        self.corecontroller.updateTimeSignature((5, 6, 7))
        info = self.corecontroller.song_info.measureInfo()
        self.assertEqual(info['time_signature'], (2, 4))
    
    def testupdateKeySignature(self):
        self.corecontroller.updateKeySignature(('C', 'Sharp', 'Major'))
        info = self.corecontroller.song_info.measureInfo()
        self.assertEqual(info['key_signature'], ('C', 'Sharp', 'Major'))
        self.corecontroller.updateKeySignature(('D', 'Natural', 'Minor'))
        info = self.corecontroller.song_info.measureInfo()
        self.assertEqual(info['key_signature'], ('D', 'Natural', 'Minor'))
        self.corecontroller.updateKeySignature(('D', 'Natural', 'Minor', 'Too long'))
        info = self.corecontroller.song_info.measureInfo()
        self.assertEqual(info['key_signature'], ('D', 'Natural', 'Minor'))
    
    def testaddMusician(self):
        self.corecontroller.addMusician('Guitar')
        self.assertEqual(self.conductor.ensemble, ['Guitar'])
        self.corecontroller.addMusician('Drum')
        self.assertEqual(self.conductor.ensemble, ['Guitar', 'Drum'])
    
    def testremoveMusician(self):
        self.conductor.ensemble = ['Piano', 'Guitar', 'Drum']
        self.corecontroller.removeMusician('Guitar')
        self.assertEqual(self.conductor.ensemble, ['Piano', 'Drum'])
        self.corecontroller.removeMusician('Drum')
        self.assertEqual(self.conductor.ensemble, ['Piano'])
        self.corecontroller.removeMusician('Drum')
        self.assertEqual(self.conductor.ensemble, ['Piano'])
        self.corecontroller.removeMusician('Piano')
        self.assertEqual(self.conductor.ensemble, [])
    
    def testfilterMusicianList(self):
        list = self.corecontroller.filterMusicianList(['acoustic'])
        self.assertEqual(list, ['acoustic_guitar'])
        list = self.corecontroller.filterMusicianList(['percussion'])
        self.assertEqual(list, ['hand_drum', 'metronome'])
        list = self.corecontroller.filterMusicianList(['acoustic', 'electric'])
        self.assertEqual(list, [])
        
    def testvalidTags(self):
        list = self.corecontroller.validTags(set(['acoustic']))
        self.assertEqual(list, ['string'])
        list = self.corecontroller.validTags(set(['string']))
        self.assertEqual(list, ['acoustic', 'electric'])
        list = self.corecontroller.validTags(set(['percussion']))
        self.assertEqual(list, [])
        
    
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import corecontroller
    import songinfo
    unittest.main()


