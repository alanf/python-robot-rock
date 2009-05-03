#! /usr/bin/env python

''' testmetronome.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Unit test for Metronome.
'''

import sys
import unittest

class CountingListener(object):
	def __init__(self):
		self.n_called = 0
	def onPulse(self, t):
		"Increases count and requests to be called back each beat."
		self.n_called += 1
		return 1.0

class DependentListener(CountingListener):
	def __init__(self):
		CountingListener.__init__(self)
		self.dependency = None
	def setDependency(self, dependency):
		self.dependency = dependency;
	def onPulse(self, t):
		assert self.dependency.n_called > self.n_called
		return CountingListener.onPulse(self, t)

class TestMetronome(unittest.TestCase):
	def setup(self):
		pass

	def testBasicAdvance(self):
		"Tests that an initial pulse is generated at time 0."
		m = Metronome()
		l = CountingListener()
		m.addListener(l)

		m.advance( 0 ) # PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

	def testAdvanceWithTempoChanges(self):
		"Tests that the rate of pulse events change with respect to tempo."
		m = Metronome()
		l = CountingListener()
		m.addListener(l)

		# Test at 60 BPM
		# Note: 1 beat = 1 second
		m.setTempo( 60 )

		m.advance( 0 ) # PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( 0 ) # NO PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() triggered unexpected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( 0.5 ) # NO PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() triggered unexpected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( 0.5 ) # PULSE
		self.assertEquals( 2, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (2, l.n_called))

		# Test tempo change, now at 120 BPM.
		# 1 beat = .5 seconds
		m.setTempo( 120 )

		m.advance( 0 ) # NO PULSE
		self.assertEquals( 2, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( 0.5 ) # PULSE
		self.assertEquals( 3, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

	def testListenerWithDelayedPulse(self):
		"Tests the delayed initial event to a Metronome listener."
		m = Metronome( 60 )
		l = CountingListener()
		m.addListener( l, 1.0 )

		m.advance( 0 ) # NO PULSE
		self.assertEquals( 0, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( 1 ) # PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

	def testPriority(self):
		m = Metronome( 60 )
		b = DependentListener() # define first to test that instantiation order indepedence
		a = CountingListener()
		b.setDependency( a )

		m.addListener( a )
		m.addListener( b )

		m.advance(0)
		m.advance(1)
		m.advance(2)
			

if __name__ == '__main__':
	sys.path.append('../robotrock/')
	from metronome import Metronome
	unittest.main()

