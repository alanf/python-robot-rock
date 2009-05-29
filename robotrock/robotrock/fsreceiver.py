''' fsreceiver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
'''

from basefsreceiver import BaseFluidsynthReceiver

class FluidsynthReceiver( BaseFluidsynthReceiver ):
    "A Receiver using Fluidsynth on the backend that outputs to speakers."

    def __init__(self, soundfont_directory, samplerate=44100):
        BaseFluidsynthReceiver.__init__( self, soundfont_directory, samplerate )
        # Start 'er up!
        self.synth.start()

