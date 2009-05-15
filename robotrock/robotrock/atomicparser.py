''' atomicparser.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

from heapq import heappush, heappop
from scoremarker import ScoreMarker
from parser import *

from atomicmetronome import ATOMIC_NOTE

class AtomicParser(object):
	"""Parses a Score and emits events at a fixed interval as defined by
	ATOMIC_NOTE.
	"""

	def __init__(self, score, receiver, delay=0):
		"""Constructor for an AtomicParser object.

		score is a Score object for which the parser reads notes from.

		receiver is a Receiver object to handle note events.

		delay is the time multiple of ATOMIC_NOTE  which the parser lags behind the marker
		within the score.
		"""

		# the coupled receiver...
		self.receiver = receiver

		self.score_marker = ScoreMarker( score )
		
		self.reset()

		# Impose a delay of note to receiver.
		self.delay = delay

	def reset(self):
		"Resets this parser."

		# A single note event from the score will require multiple
		# receiver events to be triggered at different times. This
		# priority queue will manage those deferred events.
		self.eventq = []
		self.current_beat = 0

	def onPulse(self, elapsed_beats):

		assert elapsed_beats == ATOMIC_NOTE

		# Get note events for the given window of time.
		# Structured as a map of musicians to their respective note events.
		note_events = self.score_marker.getNotes( ATOMIC_NOTE )

		# Process notes into primitive events ready for 
		# receiver consumption.
		for staff, notes in note_events.iteritems():
			self.process_notes( staff, notes )

		# Fire off current events to receiver.
		for event in self.current_events():
			self.receiver.handle( event[1] )

		# advance marker
		self.score_marker.forward( elapsed_beats )

		self.current_beat += elapsed_beats

		# returns the next time the parser is actually needed... take
		# it or leave it.
		return ATOMIC_NOTE

	def process_notes( self, staff, notes ):
		"Turn notes into receiver events."
			# FIXME After BETA release
			#       Event tuple structure will change.
			#       currently fixed size: (musician, type, tone, dynamic)
		for note in notes:
			beat = self.delay + note.start
			# Maintainers: It is vital that "Note off" events are placed in queue
			#   before "Note on" events. This ensures that Notes with equal tones
			#   and times are scheduled in the right playing order.
			event = ( beat+note.duration, (staff, "Note off", note.tone, note.dynamic) )
			heappush( self.eventq , event )
			event = ( beat, (staff, "Note on", note.tone, note.dynamic) )
			heappush( self.eventq , event )

	def current_events(self):
		"Returns an event that is scheduled to occur NOW!"

		while len( self.eventq ) > 0 and self.eventq[0][0] <= self.current_beat:
			yield heappop( self.eventq )

