''' musiciandirectory.py
    Author: Micheal Beenen
    MusicianDirectory is a tool to determine what musicians should appear on 
    the musician list, and import the musicians from the directory structure
'''

import os
import sys

class MusicianDirectory(object):

    # Assumes that each directory in the musicians directory contains only two
    # python files, the musician module and the test module. The musician module
    # should contiain a Musician constructor which points to the default
    # constructor
    def __init__(self):
	
	self.musicians = dict()
	
	try:
	    directory = os.listdir('musicians')
	except OSError:
	    print 'musicians directory not found'
	    return
	
	# search directory for musician directories
	for item in directory:
	    tags_valid = False
	    module_valid = False
	    tags_set = set()
	    # test whether the file is a valid musician directory, skip if not
	    if 'musician' not in item or not os.path.isdir('musicians\\'+item):
		continue
	    musician_directory = os.listdir('musicians\\' + item)
	    sys.path.append('musicians\\' + item)
	    
	    # search musician directory for python and info files
	    for file_name in musician_directory:
		# musician info file found
		if(file_name == 'info.txt'):
		    f = open('musicians\\' + item + '\\' + file_name, 'r')
		    line = f.readline()
		    # need to construct the tags set
		    if 'tags' in line:
			tags_valid = True
		        line = line[line.find(':')+1:len(line)]
		        line = line.strip()
		        # parse the tags line, using a comma delimiter
		        tags = line.split(',')
		        for tag in tags:
			    tag = tag.strip()
			    tags_set.add(tag)
		elif('.py' in file_name and '.pyc' not in file_name and \
		    'test' not in file_name):
		    # import the module
		    module_name = file_name[0:file_name.find('.')]
		    try:
		        __import__(module_name)
		    except ImportError:
			print 'error importing', module_name
			continue
		    # discover the constructor method
		    construct_cmd = 'constructor = sys.modules[module_name].Musician'
		    try:
		        exec construct_cmd
			module_valid = True
		    except AttributeError:
		        print module_name, 'does not have appropriate \
			     constructor named Musician'
		        continue
			
	    # if all necessary files were found and were of proper format, add
	    # the musician to the dictionary
            if not tags_valid:
		print item, 'did not contain proper info.txt with valid tags'
	    if not module_valid:
		print item, 'did not contain valid musician module'
	    if tags_valid and module_valid:
	        self.musicians[module_name] = (tags_set, constructor)
	
	print self.musicians

    # Returns a list of tuples (musicians, constructor) 
    # that satisfy the specified set of tags
    def filterMusicianList(self, tags):
        
        list = []
        for k in self.musicians.iterkeys():
           if tags.issubset(self.musicians[k][0]):
               list.append((k, self.musicians[k][1]))
            
        list.sort()
        return list           
            
            
    # Returns a list of tags that do not have an empty intersection
    # with the specified set of tags
    def validTags(self, tags):
        
        valid_list = []
        
        # Check each musicians set of tags
        for v in self.musicians.itervalues():
            if tags.issubset(v[0]):
                for member in (v[0] - tags):
                    valid_list.append(member)
        
        valid_list.sort()
        return valid_list
        
