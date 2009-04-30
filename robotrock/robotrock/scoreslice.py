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
    
    ''' Implements bracket operators (e.g. score[4]). '''
    def __getitem__(self, i):
        return [staff.measures[i] for staff in self.staffs]
    
    def next(self):
        self.current_index += 1
        try:
            result = self.__getitem__(self.current_index)
        except IndexError:
            result = None
        
        return result

    def previous(self):
        self.current_index -= 1
        if self.current_index > -1:
            return self.__getitem__(self.current_index)
        else:
            self.current_index = -1
            return None
        
if __name__ == '__main__':
    pass
        
