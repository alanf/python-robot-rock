'''testtone.py
   Author: Travis Veralrud <veralrud@cs.washington.edu>
   Tests aspects of tone.py
'''

import unittest
import sys
sys.path.append('../robotrock')
from tone import *

class TestTone(unittest.TestCase):

	def testGetTone(self):
		# Test w/ constants
		self.assertEqual( ("C", 4), getTone( MIDDLE_C, TONIC ) )
		self.assertEqual( ("D", 4), getTone( MIDDLE_C, SUPERTONIC ) )
		self.assertEqual( ("E", 4), getTone( MIDDLE_C, MEDIANT ) )
		self.assertEqual( ("F", 4), getTone( MIDDLE_C, SUBDOMINANT ) )
		self.assertEqual( ("G", 4), getTone( MIDDLE_C, DOMINANT ) )
		self.assertEqual( ("A", 4), getTone( MIDDLE_C, SUBMEDIANT ) )
		self.assertEqual( ("A#", 4), getTone( MIDDLE_C, SUBTONIC ) )
		self.assertEqual( ("B", 4), getTone( MIDDLE_C, LEADING_TONE ) )

		# Test next octave
		self.assertEqual( MIDDLE_C, getTone( ("B", 3 ), 1 ) )

	def testGetOctave(self):
		# Test relative octaves, up and down
		self.assertEqual( ("C", 5), getOctave(MIDDLE_C,  1) )
		self.assertEqual( ("C", 3), getOctave(MIDDLE_C, -1) )

if __name__ == "__main__":
	unittest.main()

