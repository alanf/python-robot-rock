#!/usr/bin/env python
''' Note.py
    Represents individual tones in the Score.
    Includes tone, octave, duration...
    Author: Alan Fineberg (af@cs.washington.edu)
'''
class NoteValues(object):
        def __init__(self):
            self.SIXTYFOURTH_NOTE = 6
            self.THIRTYSECOND_NOTE = 2 * self.SIXTYFOURTH_NOTE
            self.SIXTEENTH_NOTE = 2 * self.THIRTYSECOND_NOTE
            self.EIGHTH_NOTE = 2 * self.SIXTEENTH_NOTE
            self.QUARTER_NOTE = 2 * self.EIGHTH_NOTE
            self.HALF_NOTE = 2 * self.QUARTER_NOTE
            self.WHOLE_NOTE = 2 * self.HALF_NOTE
            
            self.QUARTER_NOTE_TRIPLET = self.WHOLE_NOTE / 3
            self.EIGHTH_NOTE_TRIPLET =  self.QUARTER_NOTE / 3
            self.SIXTEENTH_NOTE_TRIPLET = self.EIGHTH_NOTE / 3
            self.THIRTYSECOND_NOTE_TRIPLET = self.SIXTEENTH_NOTE / 3
        
        def dotted(value):
            return 3 * value // 2


class Note(object):
    ''' note_info is a dictionary with a Note's attributes fully described. '''
    note_values = NoteValues()
    def __init__(self, **note_info):
        self.__dict__.update(note_info)
                              
if __name__ == '__main__':
    note = Note(tone=('A',5), duration=('quarter'), dynamic='mezzoforte')
