''' soundfontdirectory.py
    Author:
    Defines the SoundfontDirectory class.

	File structure example:

	<<<
	# Comments
	# instrument name : source file [bank patch]
	bass guitar : rock_instruments.sf2 0 1
	drum kit : acoustic_drums.sf2 # omit bank and patch
	>>>

'''

class SoundfontDirectory(object):

	def __init__(self):
		self.instruments = {}

	def load(self, filename):
		"Loads the instruments from the given filename."
		pass

