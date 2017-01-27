#!/bin/bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
  echo "got to build OSX"
  ionic platform add ios
  ionic build
  echo "************************System info************************"
  xcodebuild -version
  xcodebuild -showsdks
  echo "npm version:"
  npm -v
  echo "node version:"
  node -v
  ionic info
elif [ "$TRAVIS_OS_NAME" = "linux" ]; then
  echo "the open source penguin"
  ionic platform add browser
  ionic build
  echo "************************System info************************"
  echo $TRAVIS_OS_NAME
  java -version
  echo "npm version:"
  npm -v
  echo "node version:"
  node -v
  ionic info
else
  echo "got to build android"
  ionic platform remove android
  ionic platform add android
  ionic build
  echo "************************System info************************"
  echo $TRAVIS_OS_NAME
  java -version
  andriod list target
  echo "npm version:"
  npm -v
  echo "node version:"
  node -v
  ionic info
fi
