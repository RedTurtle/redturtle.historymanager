#!/bin/bash
# we want to exit on errors
set -e

VIRTUALENV_BIN=`which virtualenv-2.4 || which virtualenv`
PYTHON=`which python2.4`
"$VIRTUALENV_BIN" --no-site-packages -p "$PYTHON" .

# Let's enter the virtualenv
. bin/activate
./bin/pip install https://pypi.python.org/packages/source/P/Pillow/Pillow-1.7.8.zip
# Now we have
PYTHON=`which python2.4 || which python`
ln -s plone322.cfg buildout.cfg

$PYTHON bootstrap.py
./bin/buildout
