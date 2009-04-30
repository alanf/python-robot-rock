import MusicianDirectory
import unittest

class TestMusicianDirectoryFunctions(unittest.TestCase):

    def testfilter_musician_list(self):
        list = MusicianDirectory.filter_musician_list(['acoustic'])
        self.assertEqual(['acoustic guitar'], list)
        
if __name__ == '__main__':
    unittest.main()