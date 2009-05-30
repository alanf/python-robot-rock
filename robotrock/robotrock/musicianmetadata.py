''' musicianmetadata.py
    A data structure for holding information about a particular musician
    Author: Michael Beenen <beenen34@cs.washington.edu>
'''

class MusicianMetadata(object):
    
    def __init__(self, name, tags, constructor, icon_path):
	
	self.name = name
	self.tags = tags
	self.constructor = constructor
	self.icon_path = icon_path
	
