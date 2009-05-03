''' parser.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

from heapq import heappush, heappop

class Receiver(object):
	"Receives control events from a Parser."
	def onNoteOn(self, note):
		pass
	def onNoteOff(self, note):
		pass

class Parser(object):
	def __init__(self, score, receiver):
		# the coupled score...
		self.score = score
		# the coupled receiver...
		self.receiver = receiver
		# A single note event from the score will require multiple
		# receiver events to be triggered at different times. This
		# priority queue will manage those deferred events.
		self.eventq = []
	def onPulse(self, elapsed_beats):
		# TODO for each note event in the score...
		#      ... parse it and schedule events in queue...
		#      ... and pass current events to the receiver
		return 0 # FIXME return beat-time to next event in queue

