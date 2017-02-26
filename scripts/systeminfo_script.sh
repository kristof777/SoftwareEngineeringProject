#!/bin/bash

# Author: Chris Mykota-Reid
# CMPT 371
# prints, to the console, the packages and tool versions of the main
# components of our system

echo "System info:"
echo $TRAVIS_OS_NAME
if [[ "${TRAVIS_OS_NAME}" == "android" ]]; then
  echo 'SDK Platform Android 7.1.1, API 25, revision 3'
  echo 'Android SDK Tools, revision 25.2.5'
  echo 'Android SDK Build-tools, revision 25.0.1'
  echo 'Android SDK Platform-tools, revision 25.0.3'
  echo 'Google Repository, revision 42'
  echo 'Android Support Repository, revision 42'
fi
  
java -version
echo 'npm version:'
npm -v
firefox --version
ionic info
