#! /usr/bin/env python

''' testaudiodriver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Unit test for AudioDriver.
'''

import sys
sys.path.append('../robotrock')
import unittest
from audiodriver import AudioDriver
from time import sleep

class TestAudioDriver(unittest.TestCase):

	# Tests whether thread properly responds to a halt request.
	def testStartHalt(self):
		a = AudioDriver( None ) # None is OK as play() is not called.
		print "Beginning thread..."
		a.start()
		sleep( 1.0 )
		print "Halting thread..."
		a.halt()
		a.join( 1.0 )
		self.assertEqual(False, a.running)

if __name__ == '__main__':
	unittest.main()

