import sys
sys.path.append('../shared')

from musician import Musician

class DummyMusician(object):

    def __init__(self):
        print 'constructed'
	
    def func(self):
	pass
	
def Musician():
    return DummyMusician()
