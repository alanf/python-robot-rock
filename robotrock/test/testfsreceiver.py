''' testfsreceiver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
	Tests the FluidsynthReceiver class.

	NOTE: Some tests are subjective as their success depends on audibility.
'''

import unittest
import sys
sys.path.append( "../robotrock" )

from fsreceiver import FluidsynthReceiver as Receiver
from tone import *
from dynamics import *
from time import sleep

class DummyMusician(object):
	def __init__(self):
		self.instrument = None

class TestFSReceiver(unittest.TestCase):

	def testRegistration(self):
		"Test successful registration of musicians into the synthesizer."
		r = Receiver()

		# FIXME What if there is no limit to # of musicians?
		n = len( r.available_channels )

		musicians = [DummyMusician() for x in xrange(n+1)]

		# Register
		for m in xrange(n):
			self.assertTrue( r.registerMusician( musicians[m] ) )

		# Verify admittance
		for m in xrange(n):
			self.assertTrue( r.registered_musicians.has_key( musicians[m] ) )

		# Verify capacity limit
		self.assertFalse( r.registerMusician( musicians[n] ) )

	def testUnregister(self):
		# TODO Post BETA goal
		pass

	def testHandle(self):
		"""Test event handling by playing a C-major chord.

		Note that this test is subjective as its success depends upon audio output."""
		r = Receiver()

		class Musician(object):
			def __init__(self):
				self.instrument = "FF4"

		# Manually setup directory
		r.soundfont_directory["FF4"] = "ff4sf2.sf2"

		m = Musician()
		r.registerMusician( m ) # auto-registered for BETA

		# Play C-major chord for two seconds
		event = (m, "Note on", MIDDLE_C, MEZZOFORTE )
		r.handle( event )
		event = (m, "Note on", getTone(MIDDLE_C, MEDIANT), MEZZOFORTE )
		r.handle( event )
		event = (m, "Note on", getTone(MIDDLE_C, DOMINANT), MEZZOFORTE )
		r.handle( event )
		sleep(2)

		# Release and wait two seconds
		event = (m, "Note off", MIDDLE_C, MEZZOFORTE )
		r.handle( event )
		event = (m, "Note off", getTone(MIDDLE_C, MEDIANT), MEZZOFORTE )
		r.handle( event )
		event = (m, "Note off", getTone(MIDDLE_C, DOMINANT), MEZZOFORTE )
		r.handle( event )

		sleep(2)

	def testLoadSoundfontDirectory(self):
		"""Tests the loading of instrument -> soundfont mappings."""

		r = Receiver()

		#	r.loadSoundfontDirectory("sf_directory_test.txt")

		# TODO Post BETA requirement.

		pass

if __name__ == '__main__':
	unittest.main()

