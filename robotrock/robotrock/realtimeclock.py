''' realtimeclock.py
    Defines the RealtimeClock class; conforms to Clock interface.
'''

from time import time as systime

class RealtimeClock(object):
	def time(self):
		"""Returns an absolute time in seconds since process was created."""
		return systime()

