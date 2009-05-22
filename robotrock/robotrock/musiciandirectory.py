''' musiciandirectory.py
    Author: Micheal Beenen
    MusicianDirectory is a tool to determine what musicians should appear on 
    the musician list
'''

import os
import sys

class MusicianDirectory(object):

    def __init__(self):
	
	self.musicians = dict()
	
	directory = os.listdir('musicians\\')
	#search directory for musician directories
	for item in directory:
	    tags_set = set()
	    if 'musician' not in item:
		continue
	    musician_directory = os.listdir('musicians\\' + item)
	    sys.path.append('musicians\\' + item)
	    # search musician directory for python and info files
	    for file_name in musician_directory:
		# musician info file found
		if(file_name == 'info.txt'):
		    f = open('musicians\\' + item + '\\' + file_name, 'r')
		    line = f.readline()
		    tags = line[line.find(':')+2:len(line)]
		    # parse the tags line, using a comma delimiter
		    while tags.find(',') != -1:
			front = tags[0:tags.find(',')]
			tags_set.add(front)
			tags = tags[tags.find(',') + 1: len(tags)]
		    # add the last tag
		    tags_set.add(tags)
		elif('.py' in file_name and '.pyc' not in file_name):
		    # import the module
		    #HACK
		    module_name = file_name[0:file_name.find('.')]
		    import_cmd = 'import ' + module_name
		    exec import_cmd
		    print module_name
		    constructor_name = module_name.capitalize()
		    print constructor_name
		    constructor_name = constructor_name.replace('musician', 'Musician')
		    print constructor_name
		    construct_cmd = 'constructor = sys.modules[module_name].' + constructor_name
		    print construct_cmd
		    exec construct_cmd
		    print constructor
		    #ENDHACK
	    self.musicians[item] = (tags_set, constructor)
	
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
        
