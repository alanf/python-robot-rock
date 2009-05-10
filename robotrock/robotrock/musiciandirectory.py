''' musiciandirectory.py
    Author: Micheal Beenen
    MusicianDirectory is a tool to determine what musicians should appear on 
    the musician list
'''

class MusicianDirectory(object):

    def __init__(self):
    
	#EXPORT TO SOMEWHERE OUTSIDE THE CLASS!
        self.musicians = dict(acoustic_guitar=frozenset(['acoustic', 'string']), \
	                      electric_guitar=frozenset(['electric', 'string']), \
	                      hand_drum=frozenset(['percussion']), \
			      metronome=frozenset(['percussion']))

    # Returns a list of musicians that satisfy the specified tags
    def filterMusicianList(self, tags):
        
        list = []
        for k in self.musicians.iterkeys():
           if tags.issubset(self.musicians[k]):
               list.append(k)
            
	list.sort()
        return list           
            
            
    # Returns a set of tags that do not have an empty intersection
    # with the specified list of tags
    def validTags(self, tags):
	
	valid_list = []
        
        # Check each musicians set of tags
        for v in self.musicians.itervalues():
            if tags.issubset(v):
		for member in (v - tags):
                    valid_list.append(member)
        
        valid_list.sort()
	return valid_list
        
