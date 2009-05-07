''' musiciandirectory.py
    Author: Micheal Beenen
    MusicianDirectory is a tool to determine what musicians should appear on the musician list
'''

class MusicianDirectory(object):

    def __init__(self):
    
        self.musicians = {   
                         'acoustic_guitar': frozenset(['acoustic', 'string']), 
                         'electric_guitar': frozenset(['electric', 'string']), 
                         'hand_drum': frozenset(['percussion']),
                         'metronome': frozenset(['percussion']),
                         }

    # Returns a list of musicians that satisfy the specified tags
    def filterMusicianList(self, tags):
        
        list = []
        for k in self.musicians.iterkeys():
           if tags.issubset(self.musicians[k]):
               list.append(k)
            
        return list           
            
            
    # Returns a list of tags that do not have an empty intersection
    # with the specified list of tags
    def validTags(self, tags):
    
        list = []
        

        print 'returning valid tags'
        return ['acoustic']
        
    
