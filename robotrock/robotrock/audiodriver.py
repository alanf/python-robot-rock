''' audiodriver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>

    Defines the AudioDriver class.
'''

from threading import Thread
from time import sleep
from time import time

class AudioDriver(Thread):
    """A real-time audio driver.

    Supply an instantiation of the Metronome class and begin thread with start().

    The metronome is initially halted. Use play() to begin."""

    def __init__(self, clock, metronome):
        """Constructor.

        clock: mechanism to regulate time. Must conform to Clock interface.
        metronome: generator of onPulse events. Must conform to Metronome interface. """

        Thread.__init__(self)

        self.clock = clock
        self.m = metronome

        self.running = False
        self.playing = False

    def run(self):
        "DO NOT CALL DIRECTLY. This will be called by start()."
        self.running = True
        last_time = self.clock.time()
        sleep_time = last_time % 1.0
        while self.running:
            current_time = self.clock.time()
            sleep_time += current_time
            if self.playing:
                self.m.advance( current_time - last_time )
            else:
                sleep ( 0.1 )
            last_time = current_time
            if sleep_time > 1.0:
                sleep( 0.0001 )
            sleep_time %= 1.0

    def halt(self):
        """Triggers this audio driver thread to halts this current thread.
        This may be called from another thread."""
        self.running = False

    def play(self):
        "Begin metronome onPulse event generation."
        self.playing = True

    def pause(self):
        "Stop metronome onPulse event generation."
        self.playing = False

