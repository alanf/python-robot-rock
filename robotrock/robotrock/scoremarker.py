''' scoremarker.py
    Author:
    ScoreMarker is used to obtain relative note data from a mutable
    location within a Score.
'''

class ScoreMarker(object):
	"""Keeps a position within a score and may be moved in arbitrary
	directions.

	The ScoreMarker makes it possible to extract relative note data
	from a location without having to explicitly handle measure boundaries
	and other underlying Score structure."""

	def __init__(self, score):
		"Constructor. Creates marker into the given Score."
		self.score = score
		# create a measure marker and a beat marker

	def rewind(self, n_beats):
		"Moves backward by the specified number of quarter notes."
		
		# Subtract beat marker from n_beats
			# while n_beats is > 0
		    # move the measure marker to previous
		    # get the beats / measure in current measure
		    # subtract beats / measure from n_beats
		# if n_beats < 0
		    # measure marker = previous
		    # beat marker = beats / measure + n_beats 
		pass

	def forward(self, n_beats):
		"Moves forward by the specified number of quarter notes."
		# See rewind for basic algorithm
		pass

	def getNotes(self, range):
		"""Returns the notes in the range for all staffs.

		The dictionary returned uses the staff as a key and an ordered
		list of time and note events as the values.  The time events
		are relative to the marker.

		The marker is not advanced."""
		note_events = {}
		# Should this bridge the gap across measure bars? Currently it doesn't.
		for staff in staff.score_slices[self.measure_marker]:
		    note_events[staff] = []
		    for measure in staff:
		         for note in measure.orderedNotes():
		             # if note.start is after beat offset abd note.start is before
		             # beat offset + range
		             # Maybe break early too if we want, since the list is sorted.
		             note_events[staff].append(note)
		             

		pass

		return note_events

