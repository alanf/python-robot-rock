''' fsreceiver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

# Unresolved issues: Removing a musician before scheduled notes are played

from basefsreceiver import BaseFluidsynthReceiver
from note import Note
import wave

class WaveReceiver( BaseFluidsynthReceiver ):
    "A Receiver using Fluidsynth on the backend."

    def __init__(self, soundfont_directory, samplerate=44100):
        BaseFluidsynthReceiver.__init__(self, soundfont_directory, samplerate=44100)
        # Start with no file to record to
        self.record_file = None
        self.samples = self.synth.get_samples(0) # No initial samples
        self.n_frames = 0

# Recording support is here

    def recordFile(self, file):
        """Specify the file to record.

        parameter file may be either a opened, _writable_ file object or a
        string of the filename."""
        try:
            self.record_file = wave.open( file, "w" )
            self.record_file.setsampwidth( 2 ) # 16-bit
            self.record_file.setnchannels( 2 )   # fluidsynth is stereo by default
            self.record_file.setframerate( self.samplerate )
        except:
            self.record_file = None
            print "Failed to start recording!"

    def stopRecording(self):
        if self.record_file is not None:
            print "expected number of frames =", self.n_frames
            self.record_file.close()
            print "acutal number of frames =", self.record_file.getnframes()
            self.record_file = None

    def onEndOfFrame(self, elapsed_beats):
        if self.record_file:
            n_samples = (self.samplerate * elapsed_beats) / Note.note_values.QUARTER_NOTE
            self.n_frames += n_samples / 2
            self.samples = self.synth.get_samples( n_samples / 2 ) # /2 because of stereo
            self.record_file.writeframes( self.samples )

