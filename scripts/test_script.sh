#!/bin/bash

# Author: Chris Mykota-Reid
# A helper script to allow both smoke tests to run even if one fails
# while still having the build fail if either fails

python -m unittest discover -s server-gae/ -p 'Test*.py'
screen -d -m -L ionic serve --firefox@47.0.1
sleep 50
xvfb-run protractor e2e-tests.conf.js
