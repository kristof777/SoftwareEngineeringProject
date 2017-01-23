#!/bin/bash

if [[ $TRAVIS_OS_NAME = 'osx' ]]; then
  ionic platform add ios
  ionic build
else
  ionic platform remove android
  ionic platform add android
  ionic build
fi
