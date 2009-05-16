''' fsreceiver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

# Unresolved issues: Removing a musician before scheduled notes are played

from fluidsynth import Synth
from dynamics import *

_TONE_VALUE = { # for toneToMIDICode
	'C'  :  0, 'B#' : 0,
	'C#' :  1, 'Db' : 1,
	'D'  :  2,
	'D#' :  3, 'Eb' : 3,
	'E'  :  4, 'Fb' : 4, 
	'F'  :  5, 'E#' : 5,
	'F#' :  6, 'Gb' : 6,
	'G'  :  7,
	'G#' :  8, 'Ab' : 8,
	'A'  :  9,
	'A#' : 10, 'Bb' : 10,
	'B'  : 11, 'Cb' : 11
}

def toneToMIDICode(tone):
	"Converts a tone into its respective MIDI code."

	note, octave = tone

	code = _TONE_VALUE[note] + 12 * octave

	# clamp to range [0..127]
	return min(max(0, code), 127)

def dynamicToMIDICode(dynamic):
	"Converts a dynamic value into its respective MIDI code."

	value = dynamic - MINIMUM_DYNAMIC_VALUE
	value /= MAXIMUM_DYNAMIC_VALUE - MINIMUM_DYNAMIC_VALUE
	return int(127 * value)

class FluidsynthReceiver(object):
	"A Receiver using Fluidsynth on the backend."

	def __init__(self, samplerate=44100):
		self.synth = Synth( samplerate=samplerate )
		self.available_channels = range(16)
		self.registered_staffs = {}

		self.soundfonts = {}
		self.soundfont_directory = {}

		# Start 'er up!
		self.synth.start()

	def loadSoundfontDirectory(self, filename):
		# TODO *** Post BETA feature ***
		# TODO Add support to read bank and preset
		# TODO This file format needs documentation!
		f = open(filename)
		for line in f:
			# Ignore comments
			line = line.split('#')[0].strip()
			if ':' not in line: continue
			key, value = line.split(":")
			self.soundfont_directory[key.strip()] = value.strip()

	def registerStaff(self, staff):
		"Registers a staff for inclusion into the synthesizer."

		# Reject if no vacancy
		if len( self.available_channels ) == 0:
			return False

		# Reject if already included
		if staff in self.registered_staffs:
			return False

		# Register!
		channel = self.available_channels.pop()
		self.registered_staffs[staff] = channel

		# Load instruments
		if staff.instrument not in self.soundfonts:
			try:
				sf_filename = self.soundfont_directory[staff.instrument]
				sf = self.synth.sfload(sf_filename)
				self.soundfont_directory[staff.instrument] = sf
			except:
				# TODO Error loading soundfont; best way to handle???
				self.soundfont_directory[staff.instrument] = None
				pass
		# else already available

		# Associate chennel with instrument
		# TODO Post BETA:
		#      The following values will be read from the directory.
		bank = 0
		preset = 0
		# BETA FREEZE
		sf = self.soundfont_directory[staff.instrument]
		self.synth.program_select( channel, sf, bank, preset)
		self.synth.sfont_select(channel, sf)

		# Return the good news
		return True

	def unregisterStaff(self, staff):
		"Unregisters a staff from the synthesizer."

		# Reject if not registered
		if staff not in self.registered_staffs:
			return False

		# Give back resource
		self.available_channels.append( self.registered_staffs[staff] )

		# Remove!
		self.registered_staffs.pop( staff )

		# Return the good news
		return True

	def handle(self, event):
		"Process a given event."
		# TODO After BETA, this tuple will change to have type first and
		#      event tuples will be of variable length.
		staff, type, tone, dynamic = event

		channel = self.registered_staffs.get( staff, -1 )

		# HACK HACK HACK HACK HACK
		# Auto register unknown musicians
		if channel == -1:
			self.registerStaff( staff )
			channel = self.registered_staffs.get( staff, -1 )
		# HACK HACK HACK HACK HACK

		# TODO early exit if channel == -1?

		midi_note = toneToMIDICode( tone )
		midi_vel = dynamicToMIDICode( dynamic )

		if type == "Note on":
			self.synth.noteon( channel, midi_note, midi_vel )
		elif type == "Note off":
			pass#self.synth.noteoff( channel, midi_note )

