#!/usr/bin/env python
''' scoreslice.py
    Author: Alan Fineberg (af@cs.washington.edu)
    Manipulates Staffs to produce a vertical slice of the Score. Returns
    measures.
'''
from staff import Staff

class ScoreSlice(object):
    def __init__(self, staffs):
        self.staffs = staffs
        self.current_index = -1
    
    def __getitem__(self, i):
        ''' Implements bracket operators (e.g. score[4]). '''
        return [staff.measures[i] for staff in self.staffs]
    
    def current(self):
        ''' Return the measures at current_index. '''
        return self.__getitem__(self.current_index)
        
    def next(self):
        ''' Move current_index forward and return the measures there. '''
        self.current_index += 1
        try:
            result = self.__getitem__(self.current_index)
        except IndexError:
            result = None
        
        return result

    def previous(self):
        ''' Move current_index backward and return the measures there. '''
        self.current_index -= 1
        if self.current_index > -1:
            return self.__getitem__(self.current_index)
        else:
            self.current_index = -1
            return None
        
if __name__ == '__main__':
    pass
        
