from distutils.core import setup

NAME = "Robot Rock" # print-friendly name

MY_NAME = 'robotrock' # directory name

AUTHOR = \
	"Alan Fineberg, " +\
	"Michael Beenen, " +\
	"Rick Snider, " +\
	"Tim Crossley, " +\
	"Travis Veralrud"

AUTHOR_EMAIL = "..." # TODO

# TODO: Classifiers, for look-up in trove...

CONTACT = "Alan Fineberg"

CONTACT_EMAIL = "af@cs.washington.edu"

DATA = [ 'AUTHORS',
         'CONTACT',
         'COPYING',
         'INSTALL',
         'doc/*' ] # other resources are listed in here, like so.

DESCRIPTION = "A fun, easy interactive music tool." # TODO should be better!

LICENSE = "(implicit)" # TODO

PLATFORMS = "any"

REQUIREMENTS = ['pyQt']

URL = "TODO"

VERSION = "0.0-ZFR"

setup(
	# project 
	name = MY_NAME,
	version = VERSION,
	license = LICENSE,
	url = URL,

	# author information
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	contact = CONTACT,
	contact_email = CONTACT_EMAIL,

	# descriptions
	description = DESCRIPTION,
	fullname = NAME,
	platforms = PLATFORMS,

	# packages
#	packages = [ MY_NAME ],
	package_dir = { '' : MY_NAME },
#	package_data = { MY_NAME : DATA },
	# OR
#	py_modules = [ "fluidsynth" ]

	# misc data files
#	data_files = DATA,

	# requirements
	requires = REQUIREMENTS

	)

