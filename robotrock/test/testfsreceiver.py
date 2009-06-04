''' testfsreceiver.py
    Author: Travis Veralrud <veralrud@cs.washington.edu>
    Tests the FluidsynthReceiver class.

    NOTE: Some tests are subjective as their success depends on audibility.
'''

import unittest
import sys
sys.path.append( "../robotrock" )

import fsreceiver
import basefsreceiver
Receiver = fsreceiver.FluidsynthReceiver
from tone import *
from dynamics import *
from time import sleep

class DummyStaff(object):
    def __init__(self):
        self.instrument = None

class DummyDirectory(object):
    def __init__(self):
        self.instruments = {}

class TestFSReceiver(unittest.TestCase):

    def testRegistration(self):
        "Test successful registration of staffs into the synthesizer."

        dir = {}
        dir["piano"] = ("ff4sf2.sf2", 0, 0)

        r = Receiver( dir )

        # FUTURE What if there is no limit to # of staffs?
        n = len( r.available_channels )

        staffs = [DummyStaff() for x in xrange(n+1)]

        # Register
        for s in xrange(n):
            self.assertTrue( r.registerStaff( staffs[s] ) )

        # Verify admittance
        for s in xrange(n):
            self.assertTrue( r.registered_staffs.has_key( staffs[s] ) )

        # Verify capacity limit
        self.assertFalse( r.registerStaff( staffs[n] ) )

        r.synth.delete()

    def testRegisterBogusInstrument(self):
        """Test registration of staffs with an instrument that doesn't exist within
        the directory."""

        dir = {}
        r = Receiver( dir )

        staff = DummyStaff()
        staff.instrument = "garbage can lid"

        # Should still register...
        self.assertTrue( r.registerStaff( staff ) )

        # ...and have "Invalid" soundfont association
        sf, bank, patch = r.instrument[ staff.instrument ]

        self.assertEqual( basefsreceiver.INVALID_SOUNDFONT, sf )

        r.synth.delete()

    def testUnregister(self):

        staff = DummyStaff()

        dir = {}
        r = Receiver( dir )

        n = len( r.available_channels )

        staffs = [DummyStaff() for x in xrange(n+1)]

        # Register
        self.assertTrue( r.registerStaff( staff ) )

        channel = r.registered_staffs[ staff ]

        self.assertFalse( channel in r.available_channels )

        # Unregister
        self.assertTrue( r.unregisterStaff( staff ) )

        self.assertTrue( channel in r.available_channels )

        r.synth.delete()

    def testHandle(self):
        """Test event handling by playing a C-major chord.

        Note that this test is subjective as its success depends upon audio output."""

        # Manually setup directory
        dir = {}
        dir["piano"] = ("ff4sf2.sf2", 0, 0)

        r = Receiver( dir )

        class Staff(object):
            def __init__(self):
                self.instrument = "piano"

        s = Staff()
        r.registerStaff( s ) # auto-registered for BETA

        # Play C-major chord for two seconds
        event = (s, "Note on", MIDDLE_C, MEZZOFORTE )
        r.handle( event )
        event = (s, "Note on", getTone(MIDDLE_C, MEDIANT), MEZZOFORTE )
        r.handle( event )
        event = (s, "Note on", getTone(MIDDLE_C, DOMINANT), MEZZOFORTE )
        r.handle( event )
        sleep(2)

        # Release and wait two seconds
        event = (s, "Note off", MIDDLE_C, MEZZOFORTE )
        r.handle( event )
        event = (s, "Note off", getTone(MIDDLE_C, MEDIANT), MEZZOFORTE )
        r.handle( event )
        event = (s, "Note off", getTone(MIDDLE_C, DOMINANT), MEZZOFORTE )
        r.handle( event )

        sleep(2)

        r.synth.delete()

if __name__ == '__main__':
    unittest.main()

