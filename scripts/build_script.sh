#!/bin/bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
# if we are deploying we only want to build the app 
  ionic platform add ios
  if [ "$BUILD_TYPE" = "deployment" ]; then
    ionic build ios
  else
    echo "got to build OSX"
    ionic build ios
    ionic emulate ios
    cat /Users/travis/build/CMPT371Team1/Project/platforms/ios/cordova/console.log
  fi
  echo "************************System info************************"
  xcodebuild -version
  xcodebuild -showsdks
  echo "npm version:"
  npm -v
  ionic info
elif [ "$TRAVIS_OS_NAME" = "linux" ]; then
  echo "the open source penguin"
  if [ "$BUILD_TYPE" = "deployment" ]; then
    ionic build
  else
    ionic serve
  fi
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
  if [ "$BUILD_TYPE" = "deployment" ]; then
    ionic build android --release
    ls /home/travis/build/CMPT371Team1/Project/platforms/android/build/outputs/
  else
    ionic build android
    ionic emulate android
  fi
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
