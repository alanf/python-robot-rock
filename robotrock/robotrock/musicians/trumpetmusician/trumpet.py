''' trumpet.py
    A trumpet playing musician
    Author: Michael Beenen <beenen34@cs.washington.edu> (with significant
    inspirtion from Alan Fineberg's bass musician).
'''

import activemusician
import dynamics
import note
import random
import sys
import tone

class Trumpet(activemusician.ActiveMusician):
    
    def __init__(self):
	activemusician.ActiveMusician.__init__(self)
	self.instrument = 'trumpet'
	self.last_octave = 5
	
    def compose(self, measure, window_start, window_duration, current_score_slice):
	 if window_start == 0 or self.changed:
            if self.changed:
                measure.notes = []
                self.changed = False
        
            complexity = self._complexity / 100.0
            beat_value = note.Note.note_values.HALF_NOTE
            if self._energy > 50:
                beat_value = note.Note.note_values.QUARTER_NOTE
		
	    notes = self.createRhythm(measure.time_signature[0], \
	    		beat_value)
	
	    # Determine the root note, key, and octave
	    base_octave = self.chooseOctave()
	    root = (measure.key_signature[0], base_octave)
	    self.last_octave = base_octave
	    minor = measure.key_signature[1] == 'minor'
	    
	    for my_note in notes:
                my_note.dynamic = self.chooseDynamic()
		my_note.tone = self.chooseTone(root, complexity, minor)
                measure.addNote(my_note)
		
    def chooseDynamic(self):
	rand = random.random() * self._energy
	if rand < 25:
	    return dynamics.MEZZOPIANO
	elif rand < 50:
	    return dynamics.MEZZOFORTE
	elif rand < 75:
	    return dynamics.FORTE
	else:
	    return dynamics.FORTISSIMO
		
    def chooseOctave(self):
	# TODO: Cool way to move between octaves
	return 5
		
    def chooseTone(self, root, complexity, minor=False):
	# Root note.
	rand = random.random() * complexity
	if rand < .20:
	    return root
	# The third note.
	elif rand < .40:
	    if not minor:
		return (tone.getTone(root, tone.MEDIANT))
	    else:
		return (tone.getTone(root, tone.MINOR_MEDIANT))
	# The fifth note.
	elif rand < .60:
	    return (tone.getTone(root, tone.DOMINANT))
	# The forth note.
	elif rand < .80:
	    return (tone.getTone(root, tone.SUBDOMINANT))
	# The sixth or minor seventh note.
	else:
	    if not minor:
		return (tone.getTone(root, tone.SUBMEDIANT))
	    else:
		return (tone.getTone(root, tone.SUBTONIC))
    
    def createRhythm(self, beats, base_rhythm):
	notes = []
	beat_number = 0
	current_start = 0
	measure_length = note.Note.note_values.QUARTER_NOTE * beats
	
	while current_start <= measure_length:
	    length_rand = random.random() * max(33, self._complexity) / 100.0
	    offbeat_rand = random.random() * max(33, self._complexity) / 100.0
	    
	    current_notes = []
	    
	    # Determine the rhythmic sequence of notes
	    # Comments in reference to a base rhythm of quarter note
	    # Rest
	    if length_rand < .16:
		#current_notes.append(note.Note(duration=base_rhythm, \
		#		start=current_start, rest=True))
		duration = base_rhythm
	    # Half note
	    elif length_rand < .33:
		current_notes.append(note.Note(duration=base_rhythm * 2, \
				start=current_start))
		duration = base_rhythm * 2
	    # Quarter note
	    elif length_rand < .50:
		current_notes.append(note.Note(duration=base_rhythm, \
				start=current_start))
		duration = base_rhythm
	    # Dotted Quarter note
	    elif length_rand < .67:
		current_notes.append(note.Note(duration=base_rhythm * 3 / 2, \
				start=current_start))
		duration = base_rhythm * 3 / 2
	    # Eighth note pair
	    elif length_rand < .83:
		current_notes.append(note.Note(duration=base_rhythm / 2, \
				start=current_start))
		current_notes.append(note.Note(duration=base_rhythm / 2, \
				start=current_start + base_rhythm / 2))
		duration = base_rhythm
	    # Eighth note triplets
	    else:# length_rand > .16:
		current_notes.append(note.Note(duration=base_rhythm / 3, \
				start=current_start))
		current_notes.append(note.Note(duration=base_rhythm / 3, \
				start=current_start + base_rhythm / 3))
		current_notes.append(note.Note(duration=base_rhythm / 3, \
				start=current_start + 2 * base_rhythm / 3))
		duration = base_rhythm
	    
	    if current_start + duration <= measure_length:
	        notes.extend(current_notes)
		current_start += duration
	    else:
		break
		
	return notes

def Musician():
    return Trumpet()
