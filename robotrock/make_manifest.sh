#! /bin/bash

TMP=`mktemp`

echo "INSTALL
AUTHORS
COPYING
README
./scripts/robotrock
./test/testall
" > $TMP

find . -iname "*.py" >> $TMP

cat $TMP | sort | uniq | grep . > MANIFEST

rm $TMP

