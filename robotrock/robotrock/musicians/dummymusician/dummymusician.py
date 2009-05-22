import sys
sys.path.append('../shared')

from musician import Musician

class DummyMusician(Musician):

    def __init__(self):
        print 'constructed'
	
    def func(self):
	pass
	
