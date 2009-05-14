#!/usr/bin/env python
''' testconductor.py
    Unit Tests for Conductor class.
    Author: Alan Fineberg (af@cs.washington.edu)
'''
import sys
import unittest

class TestConductor(unittest.TestCase):
    def setUp(self):
        ''' Create stub classes and create a conductor and musicians. '''
        self.test_log = []
        
        class Musician(object):
            def __init__(self, id, log):
                ''' id is used only for testing purposes. '''
                self.id = id
                self.log = log
                self.instrument = 'Jazz Flute'
            
            def compose(self, measure, start, duration):
                self.log.append(self.id)
                measure.id = self.id
        
        class SongInfo(object):
            def measureInfo(self):
                return dict(time_signature=(4, 4))
        
        class Measure(object):
            pass
            
        class Staff(dict):
            def __init__(self, instrument):
                self.measures = expandinglist.ExpandingList(Measure, parent=self)

        class Score(object):
            def __init__(self):
                self.staffs = expandinglist.ExpandingList(Staff)
        
        self.musicians = [Musician(i, self.test_log) for i in range(0, 10)]
        self.flautist = Musician(id='flautist', log='')
        self.score = Score()
        self.song_info = SongInfo()
        self.conductor = conductor.Conductor(self.score, self.song_info, staff_obj=Staff)
    
    def testCompose(self):
        ''' Each musician should write to their log items when compose is called. '''
        self.conductor.onPulse(1)
        [self.assertEqual(i, log_item) for (i, log_item) in \
                enumerate(self.test_log)]
    
    def testStartComposingAtFirstMeasure(self):
        # First add our list of musicians with ids.
        for musician in self.musicians:
            self.conductor.addMusician(musician)
        
        # Trigger a single pulse, the duration shouldn't matter.
        self.conductor.onPulse(123)
        first_measure_ids = [staff.measures[0].id for staff in self.score.staffs]
        
        for musician in self.musicians:
            self.assertTrue(musician.id in first_measure_ids)
    
    def testMeasureAdvance(self):
        ''' 
        This test ensures that the conductor correctly advances to the next
        measure based on the number of pulses and their relative values.
        '''
        # First add our list of musicians with ids.
        for musician in self.musicians:
            self.conductor.addMusician(musician)
        
        self.conductor.chunks_per_beat = 1
        
        # After these ticks, we should not have written the second measure.
        self.conductor.onPulse(1)
        self.conductor.onPulse(1)
        self.conductor.onPulse(1)
        self.conductor.onPulse(1)                
        # Get the list of measures from each staff.
        for measures in [staff.measures for staff in self.score.staffs]:
            self.assertNotEqual(measures[0].id, None)
            # I have to give the assert a callable, which is why I use lambda.
            self.assertRaises(AttributeError, lambda : measures[1].id) 
            
        # After the next pulse, we should be on the next measure.
        self.conductor.onPulse(1)
        for measures in [staff.measures for staff in self.score.staffs]:
            self.assertNotEqual(measures[1].id, None)
            self.assertRaises(AttributeError, lambda : measures[2].id) 
            
        # Just for fun, let's make sure we reach the third measure successfully.
        self.conductor.onPulse(1)
        self.conductor.onPulse(1)
        self.conductor.onPulse(1)
        self.conductor.onPulse(1)                        
        for measures in [staff.measures for staff in self.score.staffs]:
            self.assertNotEqual(measures[2].id, None)
            self.assertRaises(AttributeError, lambda : measures[3].id)
            
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
