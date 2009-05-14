
''' musicianStructured.py
    musician definition
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

from musician import Musician
import note

class MusicianStructured(Musician):
    #Definition of what a Musician is

    def __init__(self, staff, energy=50, complexity=50, time = [4,4], key = 'B'):
        self._energy = energy
        self._complexity = complexity
        '''
        self.staff = staff
        #self.current_measure = self.staff.measures.next()
        self.current_measure = []
        #self.key =  self.current_measure.key
        #self.time =  self.current_measure.time_signature
        '''
        self._key = key
        self._time = time
        self._plans = {}
        self._changed = True #if a change is made, set changed to 1
                            #set to 0 by decide method when composing
        self._durations = note.Note.note_values

    def compose(self, measure, window_start, window_duration): #called by conductor
        #deciding if it needs to update plans        
        #writing to the score
        if self._decide():
            self._write()
            self._print(measure)

    #printing _plans to the given measure
    def _print(self, measure):
        listing = self._plans.keys()
        listing.sort()
        for x in temp:
            measure.notes.append(self._plans[x])



    #functions below should be rewritten by individual musicians

    #determines if new music needs to be generated
    def _decide(self):
        return True

    #determines what is going to be played in this measure
    #defualted to be a metronome
    def _write(self):
        for x in range(self._time[0]):
            myNote = note.Note(tone=38, start=self._getStart(x), duration=self._durations.QUARTER_NOTE, rest=False)
            self._plans[x] = myNote

    #turns the numerical value val into a start value understandable by the score
    def _getStart(self, val):
        remainder = val % 1
        val -=remainder
        result = val * self._durations.QUARTER_NOTE
        val = remainder
        
        remainder = val % .5
        val -= remainder
        result += val * self._durations.EIGTH_NOTE
        val = remainder

        remainder = val % .25
        val -= remainder
        result += val * self._durations.SIXTEENTH_NOTE
        val = remainder

        remainder = val % .125
        val -= remainder
        result += val * self._durations.THIRTYSECOND_NOTE
        val = remainder

        remainder = val % .0625
        val -= remainder
        result += val * self._durations.SIXTYFOURTH_NOTE
        val = remainder

        remainder = val % .33
        val -= remainder
        result += val * self._durations.EIGTH_NOTE_TRIPLET
        return result
        


    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        self._changed = True

    @property
    def complexity(self):
        return self._complexity

    @complexity.setter
    def complexity(self, value):
        self._complexity = value
        self._changed = True

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self._changed = True

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self._changed = True
        

'''
    #print _plans to measure
    def __printToMeasure(self, measure):
        #parse _plans
        #create notes when needed
        #append notes to measure as created
        for x in range(len(_plans)):
            if (x + 1) < len(_plans): #if there is another value left in the measure
                measure.notes.append(__getNoteType(_plans[x+1] - _plans[x]))
            else:
                measure.notes.append(__getNoteType((self.time[0] + 1) - _plans[x]))
'''

'''
    def __getNoteType(diff,location):
        myNote = note.Note(tone=0, start=location, duration=self.durations.SIXTYFOURTH_NOTE, rest=True)
        location+=self.durations.SIXTYFOURTH_NOTE
        if diff == 4.0:                       #Whole note
            myNote = note.Note(tone=38, start=location, duration=self.durations.WHOLE_NOTE, rest=False)
            location+=self.durations.WHOLE_NOTE
        elif diff == 2.0:                     #half note
            myNote = note.Note(tone=38, start=location, duration=self.durations.HALF_NOTE, rest=False)
            location+=self.durations.HALF_NOTE
        elif diff == 1.0:                     #quarter note
            myNote = note.Note(tone=38, start=location, duration=self.durations.QUARTER_NOTE, rest=False)
            location+=self.durations.QUARTER_NOTE
        elif diff == .5:                    #eigth note
            myNote = note.Note(tone=38, start=location, duration=self.durations.EIGHT_NOTE, rest=False)
            location+=self.durations.EIGHT_NOTE
        elif diff == .25:                   #sixteenth note
            myNote = note.Note(tone=38, start=location, duration=self.durations.SIXTEENTH_NOTE, rest=False)
            location+=self.durations.SIXTEENTH_NOTE
        elif diff == .125:                  #32'nd note
            myNote = note.Note(tone=38, start=location, duration=self.durations.THIRTYSECOND_NOTE, rest=False)
            location+=self.durations.THIRTYSECOND_NOTE
        elif diff == .0625:                 #64'th note
            myNote = note.Note(tone=38, start=location, duration=self.durations.SIXTYFOURTH_NOTE, rest=False)
            location+=self.durations.SIXTYFOURTH_NOTE
        elif diff == .33:                   #tripolet   
            myNote = note.Note(tone=38, start=location, duration=self.durations.QUARTER_NOTE_TRIPLET, rest=False)
            location+=self.durations.QUARTER_NOTE_TRIPLET
        elif not(diff % 1.0):                 #divisible by quarter note
            myNote = note.Note(tone=0, start=location, duration=self.durations.QUARTER_NOTE, rest=True)
            location+=self.durations.QUARTER_NOTE
            measure.notes.append(myNote)
            myNote = __getNoteType(diff - 1)
        elif not(diff % .5):                #divisible by eigth note
            myNote = note.Note(tone=0, start=location, duration=self.durations.EIGHT_NOTE, rest=True)
            location+=self.durations.EIGHT_NOTE
            measure.notes.append(myNote)
            myNote = __getNoteType(diff - .5)
        elif not(diff % .25):               #divisible by sixteenth note
            myNote = note.Note(tone=0, start=location, duration=self.durations.SIXTEENTH_NOTE, rest=True)
            location+=self.durations.SIXTEENTH_NOTE
            measure.notes.append(myNote)
            myNote = __getNoteType(diff - .25)
        elif not(diff % .125):              #divisible by 32'nd note
            myNote = note.Note(tone=0, start=location, duration=self.durations.THIRTYSECOND_NOTE, rest=True)
            location+=self.durations.THIRTYSECOND_NOTE
            measure.notes.append(myNote)
            myNote = __getNoteType(diff - .125)
        elif not(diff % .0625):             #divisible by 64'th note
            myNote = note.Note(tone=0, start=location, duration=self.durations.SIXTYFOURTH_NOTE, rest=True)
            location+=self.durations.SIXTYFOURTH_NOTE
            measure.notes.append(myNote)
            myNote = __getNoteType(diff - .0625)
        else not(diff % .33):               #divisible by tripolet
            myNote = note.Note(tone=0, start=location, duration=self.durations.QUARTER_NOTE_TRIPLET, rest=True)
            location+=self.durations.QUARTER_NOTE_TRIPLET
            measure.notes.append(myNote)
            myNote = __getNoteType(diff - .33)
        return myNote
'''
