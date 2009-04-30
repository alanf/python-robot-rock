#!/usr/bin/env python
''' Note.py
    Represents individual tones in the Score.
    Includes tone, octave, duration...
    Author: Alan Fineberg (af@cs.washington.edu)
'''
class Note(object):
    ''' note_info is a dictionary with a Note's attributes fully described. '''
    def __init__(self, **note_info):
        self.__dict__.update(note_info)
        
if __name__ == '__main__':
    note = Note(tone=('A',5), duration=('quarter'), dynamic='mezzoforte')
