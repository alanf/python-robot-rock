''' audiodriver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>

    Defines the AudioDriver class.
'''

from threading import Thread
from time import sleep
from os import times
from time import time

class AudioDriver(Thread):
	"""A real-time audio driver.

	Supply an instantiation of the Metronome class and begin thread with start().

	The metronome is initially halted. Use play() to begin."""

	def __init__(self, metronome):

		Thread.__init__(self)

		self.m = metronome

		self.running = False
		self.playing = False

	def run(self):
		"DO NOT CALL DIRECTLY. This will be called by start()."
		self.running = True
		last_time = time()
		while self.running:
			current_time = time()
			if self.playing:
				self.m.advance( current_time - last_time )
			# Be nice to CPU and not burn cycles...
			# sleep( 0.001 ) # BETA: Don't worry about yet.
			last_time = current_time

	def halt(self):
		"""Triggers this audio driver thread to halts this current thread.
		This may be called from another thread."""
		self.running = False

	def play(self):
		"Begin metronome onPulse event generation."
		self.playing = True

	def pause(self):
		"Stop metronome onPulse event generation."
		self.playing = False

