''' musiciandirectory.py
    Author: Micheal Beenen
    MusicianDirectory is a tool to determine what musicians should appear on 
    the musician list, and import the musicians from the directory structure
'''

import musicianmetadata
import os
import sys

class MusicianDirectory(object):

    def __init__(self):
        ''' Assumes that each directory in the musicians directory contains only two
            python files, the musician module and the test module. The musician module
            should contiain a Musician constructor which points to the default
            constructor
        '''
        self.musicians = {}
        # Set up the musician directory path
        base_path = self.__setupPath(musicians_dir = 'musicians', shared_dir = 'shared')
        directory = os.listdir(base_path)
        
        # Search directory for musician directories
        for item in directory:
            
            # Test whether the file is a valid musician directory, skip if not
            if 'musician' not in item or \
	    		not os.path.isdir(os.path.join(base_path, item)):
                continue
            musician_directory = os.path.join(base_path,item)
	    
            musician_metadata = self.__loadMetadata(musician_directory)
            if musician_metadata is not None:
                self.musicians[item] = musician_metadata
        
    def __setupPath(self, musicians_dir, shared_dir):
        ''' Make sure necessary folders are on the system path '''
        thisDir = os.path.split(sys.modules[__name__].__file__)[0]
        base_path = os.path.join(thisDir, musicians_dir)
        sys.path.append(os.path.join(base_path, shared_dir))

        return base_path
    
    def __loadMetadata(self, directory):        
        ''' Returns musician metadata or none if directory is not
	    a valid musician folder
	'''
        tags = None
        constructor = None
        icon_path = None
        
        musician_directory = os.listdir(directory)
        # Append the musician's directory to the system path.
        sys.path.append(directory)
        # Search musician directory for musician modules, icons and info files.
        for file_name in musician_directory:
            if self.isInfoFile(file_name):
		# Read meta data line by line from the file.
                f = open(os.path.join(directory, file_name), 'r')
                tags = self.getTags(f)
                f.close()
            elif self.isIconFile(file_name):
                icon_path = os.path.join(directory, file_name)
            elif self.isMusicianModule(file_name):
                module_name = file_name.split('.')[0]
                constructor = self.getConstructor(module_name)
                
        if tags is not None and constructor is not None and icon_path is not None:
            return musicianmetadata.MusicianMetadata(module_name, \
	    		tags, constructor, icon_path)
        return None
    
    def isInfoFile(self, file_name):
	''' Determine if the file_name is the meta data text file. '''
	return file_name == 'info.txt'
	
    def isIconFile(self, file_name):
	''' The following extensions are supported:
	    png jpg bmp gif
	'''
	icon_extensions = ['.png', '.jpg', '.bmp', '.gif']
	return any(('icon' + i) in file_name for i in icon_extensions)
	
    def isMusicianModule(self, file_name):
	''' We test using string contains() instead of regex, so we use
	    two lists to exclude compiled .pyc and other similar files
	'''
	include = ['.py']
        exclude = ['.pyc', 'test', '~', '#']
	return all([(i in file_name) for i in include]) and \
            not any([(i in file_name) for i in exclude])
    
    def getTags(self, info):
	''' The tags are metadata describing musician characteristics. '''
	tags_set = set()
	for line in info:
	    line = info.readline()
	    if 'tags' in line:
		line = line.split(':')[1]
		tags = line.strip().split(',')
		for tag in tags:
		    tags_set.add(tag.strip())
		    
        return tags_set

    def getConstructor(self, module_name):
        ''' Use instrospection to get the Musician's constructor function. '''
        __import__(module_name)            
        # Discover the constructor method, if it exists.
        module = sys.modules[module_name]
        if(module.__dict__.has_key('Musician')):
            constructor = sys.modules[module_name].Musician
        return constructor
        
    def filterMusicianList(self, tags):
        ''' Returns a list of tuples (musicians, constructor, icon path) 
            that satisfy the specified set of tags
        '''
        result = []
        for k in self.musicians.iterkeys():
           if tags.issubset(self.musicians[k].tags):
               result.append(self.musicians[k])
            
        return sorted(result, lambda l, r : cmp(l.name, r.name))           
            
            
   
    def validTags(self, tags):
        ''' Returns a set of tags that do not have an empty intersection
            with the specified set of tags
	'''
        valid_set = set()
        
	for v in self.musicians.itervalues():
	    if tags.issubset(v.tags):
	        for member in (v.tags - tags):
		    valid_set.add(member)
	
	return valid_set
