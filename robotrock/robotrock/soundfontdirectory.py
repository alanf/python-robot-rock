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

def load(filename):
    """Loads the instruments from the given filename and returns a dict object
    that maps instrument names to tuples of form (filename, bank, preset).

    See module documentation for file format.
        
    Throws RuntimeError upon detecting malformed files."""

    dir = {}

    f = open(filename)

    for line in f:
        # Ignore comments
        line = line.split('#')[0].strip()
        if ':' not in line: continue
        key, values = line.split(":")
        key = key.strip()
        values = values.strip().split()

        # Bail on malformed files
        if len( values ) == 0 or len( values ) > 3:
            raise RuntimeError( "Malformed line:\n\t%s" % (line) )

        # Looks good so far...
        # FIXME What if bank, patch are not ints?
        filename = values[0].strip()
        bank = 0
        patch = 0
        if len( values ) == 2:
            patch = int( values[1] )
        if len( values ) == 3:
            bank = int( values[1] )
            patch = int( values[2] )

        # finally, add to dict
        dir[key] = ( filename, bank, patch )

    return dir

