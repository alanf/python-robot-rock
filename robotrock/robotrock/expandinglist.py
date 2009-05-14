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
        

    def __getitem__(self, i):
        ''' May expand the list by creating new objects using the given initial 
            object info.
        '''
        try:
            list.__getitem__(self, i)
        except:
            list.extend(self, [self.__default_object() for \
                            x in xrange((i + 1) - len(self))])
           
        return list.__getitem__(self, i)

    def __default_object(self):
        ''' Create an element using optional arguments, and set the element's parent. '''
        obj = apply(self.object, self.default_object_args)
        try:
            obj.__dict__.update(self.default_object_dict)
            obj.parent = self.parent
        except AttributeError:
            pass # Not all objects have dictionaries (such as list).
        
        return obj
    
    def next(self):
        ''' Move the current_index forward and return the items at that marker. 
        Always returns an object reference. '''
        self.current_index += 1
        return self.__getitem__(self.current_index)
        
    def previous(self):
        ''' Move the current_index backward and return the items at that marker.
        Returns None if we have moved the current_index before the start. '''
        self.current_index -= 1
        if self.current_index > -1:
            return self.__getitem__(self.current_index)
        else:
            self.current_index = -1
            return None
        
if __name__ == '__main__':
    expanding_list = ExpandingList(list, arg1='some_arg')
    
