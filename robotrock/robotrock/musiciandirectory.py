''' musiciandirectory.py
    Author: Micheal Beenan
    MusicianDirectory is a tool to determine what musicians should appear on the musician list
'''

class MusicianDirectory(object):

    def __init__(self):
    
        self.musicians = {'electricguitar': ['electric', 'string'], \
                     'acousticguitar': ['acoustic', 'string'], \
                     'handdrum': ['percussion'], \
                     'metronome': ['percussion']}

    def filter_musician_list(self, tags):
    
        print 'returning filtered list'
        for k in self.musicians.iteritems():
            print k
    
    def valid_tags(self, tags):

        print 'returning valid tags'
        return ['acoustic']
    
    
