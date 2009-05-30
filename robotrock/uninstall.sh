#!/bin/bash

PREFIX=`python -c 'import sys; print sys.prefix'`

echo $PREFIX

rm -rf ${PREFIX}/bin/robotrock
rm -rf ${PREFIX}/robotrockresources
rm -rf ${PREFIX}/lib/python2.6/site-packages/robotrock