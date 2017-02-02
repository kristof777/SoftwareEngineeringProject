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
  echo "SDK Platform Android 7.1.1, API 25, revision 3"
  echo "Android SDK Tools, revision 25.2.5"
  echo "Android SDK Build-tools, revision 25.0.1"
  echo "Android SDK Platform-tools, revision 25.0.3"
  echo "Google Repository, revision 42"
  echo "Android Support Repository, revision 42"
  java -version
  echo "npm version:"
  npm -v
  ionic info
fi
