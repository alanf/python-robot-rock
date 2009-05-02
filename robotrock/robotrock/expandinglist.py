#!/usr/bin/env python
''' ExpandingList.py
    Author: Alan Fineberg (af@cs.washington.edu)
    The ExpandingList class automatically grows, avoiding null references.
    So, it combines object factory behavior with list behavior.
    Use carefully, memory overflow is very possible.
'''
class ExpandingList(list):
    ''' Initialize ExpandingList with all the arguments needed to instantiate
        a default object as it grows. 
        parent -- for RobotRock, a short cut for an object to specify a 
            reference to its containing object. For an example, when
            a Measure is created in Staff.Measures.next(), its parent Staff
            is set by ExpandingList automatically.
        default_object_args -- a tuple with constructor arguments specified
            as a list.
        default_object_dict -- a dictionary, built using key=value parameters,
            used to update the default object's own dictionary.
    '''
    def __init__(self, object, parent=None, *default_object_args, **default_object_dict):
        self.object = object
        self.parent = parent
        self.default_object_args = default_object_args
        self.default_object_dict = default_object_dict
        self.current_index = -1
        
    ''' Expands the list by creating new objects using the given initial 
        object info.
    '''
    def __getitem__(self, i):
        try:
            list.__getitem__(self, i)
        except:
            list.extend(self, [self.__default_object() for \
                            x in xrange((i + 1) - len(self))])
           
        return list.__getitem__(self, i)

    # Create the object using optional arguments, and set the object's parent. 
    def __default_object(self):
        obj = apply(self.object, self.default_object_args)
        obj.__dict__.update(self.default_object_dict)
        obj.parent = self.parent
        return obj
    
    def next(self):
        self.current_index += 1
        return self.__getitem__(self.current_index)
        
    def previous(self):
        self.current_index -= 1
        if self.current_index > -1:
            return self.__getitem__(self.current_index)
        else:
            self.current_index = -1
            return None
        
if __name__ == '__main__':
    expanding_list = ExpandingList(list, arg1='some_arg')
    
