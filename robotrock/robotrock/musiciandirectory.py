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
        
	# Alias for os.path.join
        join = os.path.join
        
        # Make sure necessary folders are on the system path
        _thisDir = os.path.split(sys.modules[__name__].__file__)[0]
        base_path = join(_thisDir, 'musicians')
        sys.path.append(join(base_path, 'shared'))
        sys.path.append(_thisDir)
        
        # Locate the musician directory
        try: 
            directory = os.listdir(base_path)
        except OSError:
            print 'musicians directory not found'
            print base_path
            return
        
        # search directory for musician directories
        for item in directory:
            tags_valid = False
            module_valid = False
            tags_set = set()
            
            print item
            
            # test whether the file is a valid musician directory, skip if not
            if 'musician' not in item or not os.path.isdir(join(base_path, item)):
                continue
            musician_directory = os.listdir(join(base_path,item))
            # append the musician's directory to the system path
            sys.path.append(join(base_path, item))
            # search musician directory for python and info files
            for file_name in musician_directory:
                include = ['.py']
                exclude = ['.pyc', 'test', '~', '#']
                # musician info file found
                if(file_name == 'info.txt'):
                    f = open(join(base_path, item, file_name), 'r')
                    line = f.readline()
                    # need to construct the tags set
                    if 'tags' in line:
                        tags_valid = True
                        line = line.split(':')[1]
                        line = line.strip()
                        # parse the tags line, using a comma delimiter
                        tags = line.split(',')
                        for tag in tags:
                            tag = tag.strip()
                            tags_set.add(tag)
                    f.close()
                elif(all([(i in file_name) for i in include]) and \
                     not any([(i in file_name) for i in exclude])):
                    # import the module
                    module_name = file_name.split('.')[0]
                    print module_name
                    try:
                        __import__(module_name)
                    except ImportError:
                        print 'error importing', module_name
                        continue
                    
                    # Discover the constructor method.
                    constructor = [method for method in dir(sys.modules[module_name]) if \
                        callable(getattr(sys.modules[module_name], method)) and \
                        method == 'Musician']
                        
                    try:
                        assert(len(constructor) == 1)
                        constructor = sys.modules[module_name].Musician
			module_valid = True
                    except AssertionError:
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
    
    
    def findDataDir(self):
        return os.path.join(sys.prefix, 'robotrockresources', 'musicians')
    
    
    # Returns a list of tuples (musicians, constructor) 
    # that satisfy the specified set of tags
    def filterMusicianList(self, tags):
        
        result = []
        for k in self.musicians.iterkeys():
           if tags.issubset(self.musicians[k][0]):
               result.append((k, self.musicians[k][1]))
            
        return sorted(result)           
            
            
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
