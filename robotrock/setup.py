from distutils.core import setup
import os
import re

"""Finds filenames matching a given regular expression, in the given directory.
   Returns a list of file paths (the concatenation of dir and each matching filename)."""
def getmatchingfiles(dir, pattern):
    addPrefix = lambda file: os.path.join(dir, file)
    filteredList = filter( lambda file: re.match(pattern, file) is not None, os.listdir(dir))
    return map(addPrefix, filteredList)

NAME = "Robot Rock" # print-friendly name

MY_NAME = 'robotrock' # package name

PKG_DATA = ['musicians/*/*.py', 'musicians/*/*.txt', 'musicians/*.txt', \
 'musicians/*/*.png']

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

# contents = []
# 
# def visit(contents, dirname, files):
#     remove = []
#     for f in files:
#         if f.startswith('.'):
#             remove.append(f)
#         elif 
#             contents.append(os.path.join(dirname, f))
#     for f in remove:
#         files.remove(f)
# 
# os.path.walk('musicians', visit, contents)

DATA = [ ('robotrockresources/images', getmatchingfiles('images', '.*\.png$')),
         ('robotrockresources/soundfonts', getmatchingfiles('soundfonts', '.*\.sf2$')),
         ('robotrockresources/soundfonts', ['soundfonts/basic_set.txt']) ]

DESCRIPTION = "A fun, easy interactive music tool."

LICENSE = "MIT"

PLATFORMS = "any"

REQUIREMENTS = ['pyQt']

URL = "http://www.assembla.com/wiki/show/cse403"

VERSION = "1.0-Final"

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
	package_data = { MY_NAME : PKG_DATA },

	# misc data files
	data_files = DATA,

	# requirements
	requires = REQUIREMENTS,

	scripts = ['scripts/robotrock']

	)

