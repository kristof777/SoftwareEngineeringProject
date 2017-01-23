#!/bin/bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
  echo "got to build OSX"
  #ionic platform add ios
  #ionic build
else
  echo "got to build android"
  #ionic platform remove android
  #ionic platform add android
  #ionic build
fi
