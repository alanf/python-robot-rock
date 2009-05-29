''' basemetronome.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
	Defines Metronome, a base class for concrete implementations.
'''

DEFAULT_TEMPO = 120 # in beats per minute
MINIMUM_TEMPO =   1 

class Listener(object):
	def onPulse(self, duration):
		"""Signal that beat from metronome has occured.

		duration specifies how much time has passed since last onPulse event."""
		pass
	def onPlay(self):
		"Signal that metronome has begun playing."
		pass
	def onPause(self):
		"Signal that metronome has been paused."
		pass

class BaseMetronome(object):
	"""An object to convert time into beats with respect to a given tempo.

        Listener objects receive onPulse events from a Metronome. Through the return value from
	the onPulse event, a Listener indicates the next beat it needs the next event."""

	def __init__(self, tempo = DEFAULT_TEMPO):
		self.tempo = tempo

	def addListener(self, listener):
		"""Adds the given listener to receive onPulse() events."""
		pass

	def advance(self, elapsed_time_in_seconds):
		"""Advances the metronome's clock by given time and triggers
		the onPulse events for listeners that registered for pulse
		events in this time frame."""
		pass
		
	def setTempo(self, tempo):
		"Sets the tempo in beats per minute."
		self.tempo_in_bps = max(tempo, MINIMUM_TEMPO) / 60.0

	def getTempo(self):
		"Gets the current tempo in beats per minute."
		return self.tempo_in_bps * 60.0

	tempo = property(fget = getTempo, fset = setTempo, doc = "The tempo in beats per minute.")

	def onPlay(self):
		"Signaled when client resumes playing the metronome."
		pass
	
	def onPause(self):
		"Signaled when client halts playing the metronome."
		pass
	
