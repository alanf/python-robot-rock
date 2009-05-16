''' testsoundfontdirectory.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Tests the SoundfontDirectory class.
'''

import sys
sys.path.append('../robotrock/')
import unittest

from soundfontdirectory import *

EMPTY_FILE = "empty_soundfontdirectory.txt"
COMMENTED_FILE = "commented_soundfontdirectory.txt"
FULL_FILE = "full_soundfontdirectory.txt"
LINE_COMMENT_FILE = "line_comment_soundfontdirectory.txt"

class TestSoundfontDirectory(unittest.TestCase):

	def setUp(self):
		self.sf_dir = SoundfontDirectory()

	def testEmptyFile(self):
		"Tests loading a file that contains no data."

		self.sf_dir.load( EMPTY_FILE )

		# No instruments loaded
		self.assertEqual( 0, self.sf_dir )

	def testCommentedFile(self):
		"Tests a file that contains only comments."

		# Shouldn't fail :)
		self.sf_dir.load( COMMENTED_FILE )

		# No instruments loaded
		self.assertEqual( 0, self.sf_dir )

	def testCommentedLine(self):
		"Tests that comments may exist on lines with definitions."

		self.sf_dir.load( FULL_FILE )

		# Test existance of one instrument loaded
		self.assertEqual( 1, self.sf_dir )

	def testFullFile(self):
		"Tests a file containing each type of note specification."

		self.sf_dir.load( FULL_FILE )

		# Default bank, patch (0,0)
		self.assertEqual( ("sffile.sf2",0,0), self.sf_dir.instruments["banjo"] )
		# Default bank, specified patch (0,1)
		self.assertEqual( ("sffile.sf2",0,1), self.sf_dir.instruments["keyboard"] )
		# Specified bank, patch
		self.assertEqual( ("another.sf2",2,2), self.sf_dir.instruments["kazoo"] )

if __name__ == '__main__':
	unittest.main()

