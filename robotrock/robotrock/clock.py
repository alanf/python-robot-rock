''' clock.py
    Defines the Clock Interface.
'''

class Clock(object):
	def time(self):
		"""Returns an absolute time, according the specification defined by
		a derived class."""
		raise Exception( "Derived classes must override this method!" )

