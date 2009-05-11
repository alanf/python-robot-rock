#!/usr/bin/env python
''' testconductor.py
    Unit Tests for Conductor class.
    Author: Alan Fineberg (af@cs.washington.edu)
'''
import sys
import unittest

class TestConductor(unittest.TestCase):
    def setUp(self):
        self.test_log = []
        
        class Musician(object):
            def __init__(self, id, log):
                ''' id is used only for testing purposes. '''
                self.id = id
                self.log = log
                self.instrument = 'Jazz Flute'
            
            def compose(self, duration):
                self.log.append(self.id)
        
        class SongInfo(object):
            def measureInfo(self):
                return dict(time_signature=(4, 4))
        
        class Staff(dict):
            pass

        class Score(object):
            def __init__(self):
                self.staffs = expandinglist.ExpandingList(Staff)
        
        self.musicians = [Musician(i, self.test_log) for i in range(0, 10)]
        self.flautist = Musician(id='flautist', log='')
        self.score = Score()
        self.song_info = SongInfo()
        self.conductor = conductor.Conductor(self.score, self.song_info)
    
    def testCompose(self):
        ''' Each musician should write to their log items when compose is called. '''
        self.conductor.onPulse(1)
        [self.assertEqual(i, log_item) for (i, log_item) in \
                enumerate(self.test_log)]
    
    def testAddMusician(self):
        ''' Adding a musician appends the ensemble and the staff list. '''
        self.conductor.addMusician(self.flautist)
        self.assertTrue(self.flautist in self.conductor.ensemble)
        self.assertEquals(len(self.score.staffs), 1)
        
    def testRemoveMusician(self):
        m = self.musicians[5]
        self.conductor.addMusician(m)
        self.assertTrue(m in self.conductor.ensemble)
        self.conductor.removeMusician(m)
        self.assertFalse(m in self.conductor.ensemble)
    
    def testConductorFollowsOrder(self):
        self.conductor.order = reversed(self.musicians)
        [self.assertEqual(i, log_item) for (i, log_item) in \
                enumerate(reversed(self.test_log))]

if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import conductor
    import expandinglist
    unittest.main()
