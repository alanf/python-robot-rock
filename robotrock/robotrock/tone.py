''' tone.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Utilities for editing and specifying the tone information of notes.
'''

# The format of a tone is (note, octave), ie. ('C', 4)

MIDDLE_C = ('C', 4)

# Client should *not* rely on the values of these constants.

# name         semitone  degree
TONIC        = 0          # 1st
SUPERTONIC   = 2          # 2nd
MEDIANT      = 4          # 3rd
SUBDOMINANT  = 5          # 4th
DOMINANT     = 7          # 5th
SUBMEDIANT   = 9          # 6th
SUBTONIC     = 10         # minor 7th
LEADING_TONE = 11         # major 7th

MINOR_MEDIANT = 3

# Used in tone to value conversion. See getTone().
_TONE_VALUE = {
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

# Used to convert values to tones.  See getTone()
_VALUE_TONE = [	"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B" ]

def getTone(root, semitone):
	"""Gets the tone relative to the given root note.

	Degree is specified in semitones; constants are available."""

	note, octave = root

    # Ensure that we support lower case tones, without making 'Ab' -> 'AB'.
	code = 12 * octave + _TONE_VALUE[ note[0].upper() + note[1] ] + semitone

	return ( _VALUE_TONE[code % 12] , code / 12 )

def getOctave(tone, degree):
	"""Gets the relative octave of the given tone.

	Positive values are higher octaves, negative values are lower octaves."""
	return ( tone[0], tone[1] + degree )

