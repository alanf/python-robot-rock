#!/usr/bin/env python
''' staff.py
    Author: Alan Fineberg (af@cs.washington.edu)
    A staff represents a staff from sheet music, which is written to by a
    single Musician in the form of notated Measures.
'''
from measure import Measure
from expandinglist import ExpandingList

class Staff(object):
    ''' Any staff-specific traits such as instrument are specified with
        key-value arguments. Example: Staff(instrument='value').
    '''
    def __init__(self, **staff_info):
        self.__dict__.update(staff_info)
        self.measures = ExpandingList(Measure, \
                        parent=self, key=('C', '#', 'maj'), time_signature=(4, 4))
        
if __name__ == '__main__':
    s = Staff(instrument='Banjo')

