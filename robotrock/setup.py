from distutils.core import setup

### This section builds the guiResources file needed for images and such. ###
### Warning: Building with sdist currently does not ###
###    include the original images or the qrc file  ###

### This lack of inclusion of source images, etc. is currently listed as a bug under
#    ticket number 77

import os.path as path
import os
GUI_GENERATED = path.abspath("robotrock/guiResources.py")
GUI_SOURCE = path.abspath("robotrock/guiResources.qrc")

if not path.exists(GUI_GENERATED) or path.getmtime(GUI_GENERATED) < path.getmtime(GUI_SOURCE):
    print "generating GUI resource file"
    os.system('pyrcc4 -o "%s" "%s"' % (GUI_GENERATED, GUI_SOURCE))


### End of GUI resource generating code ###
###########################################

NAME = "Robot Rock" # print-friendly name

MY_NAME = 'robotrock' # directory name

AUTHOR = \
	"Alan Fineberg, " +\
	"Michael Beenen, " +\
	"Rick Snider, " +\
	"Tim Crossley, " +\
	"Travis Veralrud"

AUTHOR_EMAIL = "cse403-robot-rock@cs.washington.edu"

# TODO: Classifiers, for look-up in trove...

CONTACT = "Alan Fineberg"

CONTACT_EMAIL = "af@cs.washington.edu"

DATA = [ ('robotrockresources/sounds', ['scripts/HS_R8_Drums.sf2']) ] # other resources are listed in here, like so.

DESCRIPTION = "A fun, easy interactive music tool." # TODO should be better!

LICENSE = "MIT"

PLATFORMS = "any"

REQUIREMENTS = ['pyQt']

URL = "http://www.assembla.com/wiki/show/cse403"

VERSION = "0.0-BETA"

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
	packages = [ MY_NAME ],
	package_dir = { MY_NAME : MY_NAME },
#	package_data = { MY_NAME : DATA },
	# OR
#	py_modules = [ "fluidsynth" ]

	# misc data files
	data_files = DATA,

	# requirements
	requires = REQUIREMENTS,

	scripts = ['scripts/robotrock']

	)

