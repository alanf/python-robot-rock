''' basefsreceiver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

# Unresolved issues: Removing a musician before scheduled notes are played

from fluidsynth import Synth
from dynamics import *

# HACK HACK for release
import sys
SOUNDFONT_PATH = sys.prefix + '/robotrockresources/soundfonts/'
# HACK HACK

# Maximum number of audio channels available
MAX_CHANNELS  = 16
# Value for an invalid soundfont reference
INVALID_SOUNDFONT = -1
# Gain for fluidsynth
FLUIDSYNTH_GAIN = 0.6

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


class BaseFluidsynthReceiver(object):
    "A Receiver using Fluidsynth on the backend."

    def __init__(self, soundfont_directory, samplerate=44100):
        self.synth = Synth( gain=FLUIDSYNTH_GAIN, samplerate=samplerate  ) 
        self.available_channels = range( MAX_CHANNELS )
        self.registered_staffs = {}
        self.samplerate = samplerate

        # Maps each instrument to an UNLOADED soundfont file, bank and patch
        self.sfdir = soundfont_directory

        # Maps a filename a loaded sound font
        self.soundfonts = {}

        # Maps each instrument to a LOADED soundfont, bank, patch
        self.instrument = {}

    def turnOffNotesInChannel(self, channel):
        "Turns off playing all notes for the given channel."
        for n in xrange(128):
            self.synth.noteoff( channel, n )

    def registerStaff(self, staff):
        "Registers a staff for inclusion into the synthesizer."

        instrument = staff.instrument

        # Reject if no vacancy
        if len( self.available_channels ) == 0:
            return False

        # Reject if already included
        if staff in self.registered_staffs:
            return False

        # Register!
        channel = self.available_channels.pop()
        self.registered_staffs[staff] = channel

        # Load sound
        if instrument not in self.instrument:
            # Instrument has no associated soundfont yet, so look it up.
            sf_info = self.sfdir.get(instrument, (None,0,0) )
            sf_filename, bank, patch = sf_info
            # Ensure soundfont associated with instrument is loaded...
            if sf_filename is None:
                self.soundfonts[ instrument ] = INVALID_SOUNDFONT
            elif sf_filename not in self.soundfonts:
                sf = self.synth.sfload( SOUNDFONT_PATH + sf_filename ) # INVALID_SOUNDFONT on failure
                self.soundfonts[ instrument ] = sf
            # Finally, place in loaded instrument directory
            self.instrument[ instrument ] = ( self.soundfonts[ instrument ], bank, patch )

        # Associate channel with instrument
        sf, bank, patch = self.instrument[ instrument ]
        if sf is not -1:
            self.synth.program_select( channel, sf, bank, patch)
            self.synth.sfont_select(channel, sf)

        # Return the good news
        return True

    def unregisterStaff(self, staff):
        """Unregisters a staff from the synthesizer.  Allows its resource to be
        reused by other staffs."""

        # Reject if not registered
        if staff not in self.registered_staffs:
            return False

        # Give back resource
        self.available_channels.append( self.registered_staffs[staff] )

        # Turn off all notes for this channel
        self.turnOffNotesInChannel( self.registered_staffs[staff] )
        
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

        # Bail if staff doesn't have a channel
        # Note that pending "Note on" events from recently unregistered staffs
        # will fall out here.
        if channel == -1:
            return

        midi_note = toneToMIDICode( tone )
        midi_vel = dynamicToMIDICode( dynamic )

        if type == "Note on":
            self.synth.noteon( channel, midi_note, midi_vel )
        elif type == "Note off":
            self.synth.noteoff( channel, midi_note )

    def onPlay(self):
        "Does nothing."
        pass

    def onPause(self):
        "Turn all notes off."
        for ch in xrange(MAX_CHANNELS):
            self.turnOffNotesInChannel( ch )

    def onEndOfFrame(self, elapsed_beats):
        """Opportunity signal for receiver to operate at end of a frame.

        By default, do nothing."""
        pass

