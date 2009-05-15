
''' musicianStructured.py
    musician definition
    Author: Rich Snider <mrsoviet@cs.washington.edu>
'''

from musician import Musician
import note

#definition of the recommended musician structure.
#note: one does NOT have to follow this structure to make a working musician
#note: the default musician is a metronome as defined below
class MusicianStructured(Musician):

    #initialize the general musician
    def __init__(self, energy=50, complexity=50, time = (4,4), key = ('B', 'major')):
        self._energy = energy
        self._complexity = complexity
        '''
        self.staff = staff
        #self.current_measure = self.staff.measures.next()
        self.current_measure = []
        #self.key =  self.current_measure.key
        #self.time =  self.current_measure.time_signature
        '''
        self.instrument = 'metronome'
        self._key = key
        self._time = time
        self._plans = {}
        self._changed = True #if a change is made, set changed to 1
                            #set to 0 by decide method when composing
        self._durations = note.Note.note_values

    #composes to the given measure if it needs to
    #measure is the measure being composed to
    #window_start is the start of the part of the measure that needs to be composed
    #window_duration is the length of the measure that needs to be composed
    #note: this structure ignores window_start and window_duration for the most
    #   part, they are mainly for allowing musicians to run dynamically
    def compose(self, measure, window_start, window_duration): #called by conductor
        if not(self._time == measure.time_signature):
            self._time = measure.time_signature
            self._changed = True
        if not(self._key == measure.key_signature):
            self._key = measure.key_signature
            self._changed = True
        if measure.notes == [] or window_start == 0:
            self._changed = True
            
        if self._decide():
            self._write()
            self._print(measure)

    #printing _plans (internal data structure) to the given measure
    def _print(self, measure):
        listing = self._plans.keys()
        for x in listing:
            measure.notes.append(self._plans[x])

    #turns the numerical value val into a start value understandable by the
    #   score
    def _getStart(self, val):
        (val, remainder) = self.__shave(val, 1)
        result = val * self._durations.QUARTER_NOTE
        val = remainder

        if not(val % .0625):
            (val, remainder) = self.__shave(val, .5)
            result += val  * self._durations.EIGHTH_NOTE
            val = remainder

            (val, remainder) = self.__shave(val, .25)
            result += val  * self._durations.SIXTEENTH_NOTE
            val = remainder

            (val, remainder) = self.__shave(val, .125)
            result += val  * self._durations.THIRTYSECOND_NOTE
            val = remainder

            (val, remainder) = self.__shave(val, .0625)
            result += val * self._durations.SIXTYFOURTH_NOTE

        else:   #triplets probably dont work, untested
            (val, remainder) = self.__shave(val, .33)
            result += val * self._durations.EIGHTH_NOTE_TRIPLET
        
        return result

    #helper for _getStart, does the work of figuring out how many
    #   of this type of note need to be skipped.
    #returns (val, remainder) where val is the number of this note
    #   to be skipped and remainder is how much of the measure is
    #   left to be skipped
    def __shave(self, val, amount):
        remainder = val % amount
        val -=remainder
        val = int(val/amount)
        return (val, remainder)

    #property for energy
    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        self._changed = True

    #property for complexity
    @property
    def complexity(self):
        return self._complexity

    @complexity.setter
    def complexity(self, value):
        self._complexity = value
        self._changed = True

    #property for time
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self._changed = True

    #property for key 
    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self._changed = True
        


    #functions below should be rewritten by individual musicians

    #determines if new music needs to be generated
    def _decide(self):
        return True

    #determines what is going to be played in this measure
    #defualted to be a metronome
    def _write(self):
        for x in range(self._time[0]):
            myNote = note.Note(tone=38, start=self._getStart(x+1), duration=self._durations.QUARTER_NOTE, rest=False)
            self._plans[x+1] = myNote


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
