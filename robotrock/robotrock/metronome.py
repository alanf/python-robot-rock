''' metronome.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

from heapq import heappush, heappop

DEFAULT_TEMPO = 120 # in beats per minute
MINIMUM_TEMPO =   1 
MAXIMUM_TEMPO = 360 # NOTE: arbitrary

class Metronome(object):
	"""An object to convert time into beats with respect to a given tempo.

        Listener objects receive onPulse events from a Metronome. Through the return value from
	the onPulse event, a Listener indicates the next beat it needs the next event."""

	def __init__(self, tempo = DEFAULT_TEMPO):
		self.listeners = []
		self.setTempo( tempo )
		self.heap = []
		self.current_beat = 0.0
		# The priority counter keeps track of the priority values given to added listeners.
		# This priority ensures Listener ordering when two Listeners are called upon
		# the same beat.
		self.priority_counter = 0
	def addListener(self, listener, next_pulse = 0.0):
		"""Adds the given listener to receive onPulse() events.
		next_pulse specifies the delay in beat when the listener expects
		to receive its first event; default is immediate at next
		call to advance()."""
		heappush( self.heap, (self.current_beat + next_pulse, self.priority_counter, listener))
		self.priority_counter += 1

	def advance(self, elapsed_time_in_seconds):
		"""Advances the metronome's clock by given time and triggers
		the onPulse events for listeners that registered for pulse
		events in this time frame.
		
		Each listener will only be called once in this advancement
		period, so they may make use of the given elapsed time."""

		elapsed_beats = elapsed_time_in_seconds * self.tempo_in_bps

		self.current_beat += elapsed_beats
		
		processed_listeners = []

		# Call onPulse for all expecting listeners once only.
		while len(self.heap) > 0 and self.heap[0][0] <= self.current_beat:
			listener = heappop( self.heap )[-1]
			next_t = listener.onPulse( elapsed_beats )
			processed_listeners.append( (self.current_beat + next_t, listener) )

		# With processing complete, add listeners back on to heap.
		for l in processed_listeners:
			heappush( self.heap, l )

		# FIXME Consider floating point errors!
		#       Reseting current beat and adjusting listeners will
		#       solve this issue.

	def setTempo(self, tempo):
		"Sets the tempo in beats per minute."
		if tempo < MINIMUM_TEMPO:
			tempo = MINIMUM_TEMPO
		elif tempo > MAXIMUM_TEMPO:
			tempo = MAXIMUM_TEMPO
		self.tempo_in_bps = tempo / 60.0

	def getTempo(self):
		"Gets the current tempo in beats per minute."
		return self.tempo_in_bps * 60.0

