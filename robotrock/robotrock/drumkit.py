''' drumkit.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Utility to map drum names to MIDI values via a Note's tone.
    Will work with any drum kit conforming to General MIDI drum kit spec.
'''

# WORK IN PROGRESS!!!
# keys should be lower case, values should be tone tuples

DrumKit = {
	"Acoustic Bass Drum" : ('B', 2),
	"Bass Drum 1" : ('C', 3),
	"Side Stick" : 37,
	"Acoustic Snare" : ('D', 3),
	"Hand Clap" : ('D#', 3),
	"Electric Snare" : ('E', 3),
	"Low Floor Tom" : ('F', 3),
	"closed hi-hat" : ('F#', 3),
	"High Floor Tom" : 43,
	"Pedal Hi-Hat" : 44,
	"Low Tom" : 45,
	"open hi-hat" : ('A#', 3),
	"Low-Mid Tom" : 47,
	"Hi-Mid Tom" : 48,
	"crash cymbal 1" : ('C#', 4),
	"High Tom" : ('D', 4),
	"Ride Cymbal 1" : 51,
	"Chinese Cymbal" : 52,
	"Ride Bell" : 53,
	"Tambourine" : 54,
	"Splash Cymbal" : 55,
	"Cowbell" : ('G', 4),
	"Crash Cymbal 2" : 57,
	"Vibraslap" : 58,
	"Ride Cymbal 2" : 59,
	"Ride Cymbal 2" : 59,
	"hi bongo" : ('C', 5),
	"low bongo" : ('C#', 5),
	"mute hi Conga" : ('D', 5),
	"open hi Conga" : 63,
	"low conga" : ('E', 5),
	"High Timbale" : 65,
	"Low Timbale" : 66,
	"high agogo" : ('G', 5),
	"Low Agogo" : 68,
	"Cabasa" : 69,
	"Maracas" : 70,
	"Short Whistle" : 71,
	"long whistle" : ('C', 6),
	"Short Guiro" : 73,
	"Long Guiro" : 74,
	"claves" : ('D#', 6),
	"hi wood block" : ('E', 6),
	"Low Wood Block" : 77,
	"Mute Cuica" : 78,
	"Open Cuica" : 79,
	"Mute Triangle" : 80,
	"Open Triangle" : 81
}

