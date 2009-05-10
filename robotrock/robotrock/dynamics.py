''' Constants for note dynamics.
    Author: Travis Veralrud <veralrud@attu.cs.washington.edu>

    The dynamic is coupled with note data to describe the force with which a
    note is played.
'''

MINIMUM_DYNAMIC_VALUE = 0.0
MAXIMUM_DYNAMIC_VALUE = 1.0

# The following function only serves purpose if the above values change.
# (As is, the function is a long winded way of saying f(x) = x!)
def calc_dynamic( value ):
	"Calculates dynamic constant from value in range [0..1]."
	value *= MAXIMUM_DYNAMIC_VALUE - MINIMUM_DYNAMIC_VALUE
	return MINIMUM_DYNAMIC_VALUE + value

# softer
PIANISSIMO = calc_dynamic( 0.125 )
PIANO      = calc_dynamic( 0.25  )
MEZZOPIANO = calc_dynamic( 0.375 )
MEZZOFORTE = calc_dynamic( 0.5   )
FORTE      = calc_dynamic( 0.75  )
FORISSIMO  = calc_dynamic( 0.875 )
# louder

DEFAULT_DYNAMIC = MEZZOFORTE

