#! /usr/bin/env python

''' testmetronome.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Unit test for AtomicMetronome.
'''

import unittest
import sys
sys.path.append('../robotrock/')
from atomicmetronome import *

class CountingListener(object):
	def __init__(self):
		self.n_called = 0
	def onPulse(self, t):
		"Increases count and requests to be called back each beat."
		self.n_called += 1
		return 1.0

class TestAtomicMetronome(unittest.TestCase):
	def setup(self):
		pass

	def testConstants(self):
		"Tests that calculated constants are of usable values."
		self.assertTrue( ATOMIC_NOTE > 0, "Constant ATOMIC_NOTE must be positive value." )

	def testBasicAdvance(self):
		"""Tests that an initial pulse is generated at time 0.

		The first beat should only be generated once."""
		m = AtomicMetronome()
		l = CountingListener()
		m.addListener(l)

		m.advance( 0 ) # PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( 0 ) # NO PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() triggered unexpected onPulse(): expected %d, got %d." % (1, l.n_called))

	def testAdvanceWithTempoChanges(self):
		"Tests that the rate of pulse events change with respect to tempo."
		m = AtomicMetronome()
		l = CountingListener()
		m.addListener(l)

		# Test at 60 BPM
		# Note: 1 beat = 1 second
		m.tempo = 60

		m.advance( 0 ) # PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( 0 ) # NO PULSE
		self.assertEquals( 1, l.n_called, "Metronome.advance() triggered unexpected onPulse(): expected %d, got %d." % (1, l.n_called))

		m.advance( ATOMIC_BEAT ) # PULSE
		self.assertEquals( 2, l.n_called, "Metronome.advance() triggered unexpected onPulse(): expected %d, got %d." % (2, l.n_called))

		m.advance( ATOMIC_BEAT ) # PULSE
		self.assertEquals( 3, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (3, l.n_called))

		# Test tempo change, now at 120 BPM.
		# 1 beat = .5 seconds
		m.tempo = 120

		m.advance( 0 ) # NO PULSE
		self.assertEquals( 3, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (3, l.n_called))

		m.advance( ATOMIC_BEAT / 2 ) # PULSE
		self.assertEquals( 4, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (4, l.n_called))

	def testOverProduce(self):
		"Test advance method receiving large window of time."

		m = AtomicMetronome()
		l = CountingListener()
		m.addListener(l)

		# Test at 60 BPM
		# Note: 1 beat = 1 second
		m.tempo = 60

		m.advance( ATOMIC_BEAT * 5 ) # Should trigger 1 onPulse(), not 5
		self.assertEquals( 1, l.n_called, "Metronome.advance() did not trigger expected onPulse(): expected %d, got %d." % (1, l.n_called))


if __name__ == '__main__':
	unittest.main()

