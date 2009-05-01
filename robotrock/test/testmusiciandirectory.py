import unittest
import sys

class TestMusicianDirectory(unittest.TestCase):

    def testfilter_musician_list(self):
        list = MusicianDirectory.filter_musician_list(['acoustic'])
        self.assertEqual(['acoustic guitar'], list)
        
if __name__ == '__main__':
    sys.path.append('../robotrock/')
    import musiciandirectory
    unittest.main()