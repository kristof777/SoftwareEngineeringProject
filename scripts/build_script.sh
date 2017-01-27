#!/bin/bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
  echo "got to build OSX"
  ionic platform add ios
  ionic build
  echo "************************System info************************"
  xcodebuild -version
  xcodebuild -showsdks
  npm -v
  npm ls
elif [ "$TRAVIS_OS_NAME" = "linux" ]; then
  echo "the open source penguin"
  ionic platform add browser
  ionic build
  echo "************************System info************************"
  echo $TRAVIS_OS_NAME
  java -version
  npm -v
  npm ls
else
  echo "got to build android"
  ionic platform remove android
  ionic platform add android
  ionic build
  echo "************************System info************************"
  echo $TRAVIS_OS_NAME
  java -version
  andriod list target
  npm -v
  npm ls
fi
