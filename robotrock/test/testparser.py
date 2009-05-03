#! /usr/bin/env python

''' testparser.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Unit test for Parser.
'''

import sys
sys.path.append('../robotrock/')

from parser import *
import unittest

class ParserReceiver(object):

	def __init__(self):
		self.events = []

	def onNoteOn(self, note):
		self.events.append( ("NOTE ON") )

	def onNoteOff(self, note):
		self.events.append( ("NOTE OFF") )

class TestParser(unittest.TestCase):

	def setup(self):
		pass

	def test(self):
#		score = Score()
		# TODO Create score with a single quarter note at beat zero.
		
#		p = Parser(score)
#		r = ParserReceiver()
#		p.setReceiver( r )
		
#		t = p.onPulse( 0 )

#		self.assertEqual(QUARTER_NOTE, t)

		

#		p.onPulse( 0 )
		pass

if __name__ == '__main__':
        unittest.main()

