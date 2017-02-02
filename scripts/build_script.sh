#!/bin/bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
  echo "got to build OSX"
  ionic platform add ios
  ionic build ios
  ionic emulate ios
  echo "************************System info************************"
  xcodebuild -version
  xcodebuild -showsdks
  echo "npm version:"
  npm -v
  ionic info
elif [ "$TRAVIS_OS_NAME" = "linux" ]; then
  echo "the open source penguin"
  ionic serve
  echo "************************System info************************"
  echo $TRAVIS_OS_NAME
  java -version
  echo "npm version:"
  npm -v
  ionic info
else
  echo "got to build android"
  export JAVA_HOME=/usr/lib/jvm/java-8-oracle
  ionic platform remove android
  ionic platform add android
  ionic build android
  ionic emulate android
  echo "************************System info************************"
  echo $TRAVIS_OS_NAME
  java -version
  andriod list target
  echo "npm version:"
  npm -v
  ionic info
fi
