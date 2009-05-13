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

	def rewind(self, n_beats):
		"Moves backward by the specified number of quarter notes."
		pass

	def forward(self, n_beats):
		"Moves forward by the specified number of quarter notes."
		pass

	def getNotes(self, range):
		"""Returns the notes in the range for all staffs.

		The dictionary returned uses the staff as a key and an ordered
		list of time and note events as the values.  The time events
		are relative to the marker.

		The marker is not advanced."""

		note_events = {}

		pass

		return note_events

