''' atomicmetronome.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    A flavor of Metronome that operates at small, fixed beats.
'''

import basemetronome
from note import Note

# Discrete number of calls per beat. This effectively defines the
# resolution of the atomic parser.
# NOTE 2**4 * 3 adds support for 64th standard notes (quarter / 16)
#      but only eighth triplets (quarter / 3).
DIVISIONS_PER_QUARTER_NOTE = 2**4 * 3
# Length between Listener's onPulse() event generation
ATOMIC_BEAT = 1.0 / DIVISIONS_PER_QUARTER_NOTE
# Value to report to listeners
# This value directly corresponds to DIVISIONS_PER_QUARTER_NOTE
ATOMIC_NOTE = Note.note_values.QUARTER_NOTE // DIVISIONS_PER_QUARTER_NOTE

class AtomicMetronome(basemetronome.BaseMetronome):
	"""An object to convert time into beats with respect to a given tempo.
	This Metronome will generate onPulse events at a fixed rate.

	Listener objects receive onPulse events from a Metronome."""

	def __init__(self, tempo = basemetronome.DEFAULT_TEMPO):
		self.listeners = []
		self.tempo = tempo
		self.current_beat = ATOMIC_NOTE

	def addListener(self, listener):
		"""Adds the given listener to receive onPulse() events."""
		self.listeners.append( listener )

	def advance(self, elapsed_time_in_seconds):
		"""Advances the metronome's clock by given time and triggers
		the onPulse events for listeners that registered for pulse
		events in this time frame.

		Each listener will only be called once in this advancement
		period, so they may make use of the given elapsed time."""

		elapsed_beats = elapsed_time_in_seconds * self.tempo_in_bps
		self.current_beat += elapsed_beats

		# Call onPulse for all listeners.
		if self.current_beat / ATOMIC_BEAT >= 1.0:
			for listener in self.listeners:
				listener.onPulse( ATOMIC_NOTE )

		self.current_beat %= ATOMIC_BEAT

	def onPlay(self):
		"Pass play signal to all listeners."
		for L in self.listeners:
			L.onPlay()

	def onPause(self):
		"Pass pause signal to all listeners."
		for L in self.listeners:
			L.onPause()

