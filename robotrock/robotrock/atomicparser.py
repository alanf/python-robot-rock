''' atomicparser.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

from heapq import heappush, heappop
from scoremarker import ScoreMarker
from parser import *

from atomicmetronome import ATOMIC_NOTE
import basemetronome

class AtomicParser(basemetronome.Listener):
	"""Parses a Score and emits events at a fixed interval as defined by
	ATOMIC_NOTE.
	"""

	def __init__(self, score, receivers):
		"""Constructor for an AtomicParser object.

		score is a Score object for which the parser reads notes from.

		receiver is a list of Receiver objects to handle note events.
		"""

		# the coupled receivers...
		self.receivers = receivers

		self.score_marker = ScoreMarker( score )
		
		self.reset()

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
			for R in self.receivers:
				R.handle( event[-1] )

		# Signal end of frame
		for R in self.receivers:
			R.onEndOfFrame( elapsed_beats )

		# advance marker
		self.score_marker.forward( elapsed_beats )

		self.current_beat += elapsed_beats

		# returns the next time the parser is actually needed... take
		# it or leave it.
		return ATOMIC_NOTE

	def onPlay(self):
		"Forward signal to receiver."
		for R in self.receivers:
			R.onPlay()

	def onPause(self):
		"Forward signal to receiver."
		for R in self.receivers:
			R.onPause()

	def registerStaff(self, staff):
		"Let receivers know that staff is to be registered."
		for R in self.receivers:
			R.registerStaff( staff )

	def unregisterStaff(self, staff):
		"Let receivers know that staff is to be unregistered."
		for R in self.receivers:
			R.unregisterStaff( staff )

	def process_notes( self, staff, notes ):
		"Turn notes into receiver events."
			# FIXME After BETA release
			#       Event tuple structure will change.
			#       currently fixed size: (staff, type, tone, dynamic)
		for note in notes:
			beat = self.current_beat + note.start
			event = ( beat+note.duration, (staff, "Note off", note.tone, note.dynamic) )
			heappush( self.eventq , event )
			event = ( beat, (staff, "Note on", note.tone, note.dynamic) )
			heappush( self.eventq , event )

	def current_events(self):
		"Returns an event that is scheduled to occur NOW!"

		# Sort so "Note off" goes first
		# Does so via a bucket sort
		type_bucket = {}
		type_bucket["Note on"] = []
		type_bucket["Note off"] = []

		while len( self.eventq ) > 0 and self.eventq[0][0] <= self.current_beat:
			event = heappop(self.eventq)
			type_bucket[event[-1][1]].append( event )

		current_events = []

		for event in type_bucket["Note off"]:
			current_events.append(event)

		for event in type_bucket["Note on"]:
			current_events.append(event)

		for event in current_events:
			yield event

