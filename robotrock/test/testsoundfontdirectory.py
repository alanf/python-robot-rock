''' testsoundfontdirectory.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Tests the SoundfontDirectory class.
'''

import sys
sys.path.append('../robotrock/')
import unittest

import soundfontdirectory

EMPTY_FILE = "empty_soundfontdirectory.txt"
COMMENTED_FILE = "commented_soundfontdirectory.txt"
FULL_FILE = "full_soundfontdirectory.txt"
LINE_COMMENT_FILE = "line_comment_soundfontdirectory.txt"
TAINTED_FILE = "tainted_soundfontdirectory.txt"

class TestSoundfontDirectory(unittest.TestCase):

    def testEmptyFile(self):
        "Tests loading a file that contains no data."

        d = soundfontdirectory.load( EMPTY_FILE )

        # No instruments loaded
        self.assertEqual( 0, len( d ) )

    def testCommentedFile(self):
        "Tests a file that contains only comments."

        # Shouldn't fail :)
        d = soundfontdirectory.load( COMMENTED_FILE )

        # No instruments loaded
        self.assertEqual( 0, len( d ) )

    def testCommentedLine(self):
        "Tests that comments may exist on lines with definitions."

        d = soundfontdirectory.load( LINE_COMMENT_FILE )

        # Test existance of one instrument loaded
        self.assertEqual( 1, len( d ) )

    def testFullFile(self):
        """Tests a file containing each type of instrument to soundfont
        specification."""

        d = soundfontdirectory.load( FULL_FILE )

        # Default bank, patch (0,0)
        self.assertEqual( ("sffile.sf2",0,0), d["banjo"] )
        # Default bank, specified patch (0,1)
        self.assertEqual( ("sffile.sf2",0,1), d["keyboard"] )
        # Specified bank, patch
        self.assertEqual( ("another.sf2",2,2), d["kazoo"] )

    def testTaintedFile(self):
        """Tests a file with syntax errors."""
        try:
            d = soundfontdirectory.load( TAINTED_FILE )
            raise Exception("Should have thrown RuntimeError exception!")
        except RuntimeError:
            pass # Actually, all is OK!

if __name__ == '__main__':
    unittest.main()

