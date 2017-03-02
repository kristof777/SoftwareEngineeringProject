#!/bin/bash

# Author: Chris Mykota-Reid :>
# This script calls the commands required to compile (TODO: TESTING)
# and emulate our program

set -ev

# Builds the ios app.  If we are deploying builds a release version, otherwise
# builds and emulates the app for testing.
ios_build(){
  ionic platform add ios
  if [[ "${BUILD_TYPE}" == "deployment" ]]; then
    ionic build ios
  else
    ionic build ios
    ionic emulate ios
    cat /Users/travis/build/CMPT371Team1/Project/platforms/ios/cordova/console.log
  fi
}

# Builds the browser version of our app 
# TODO: THIS PROBABLY ISN'T WORKING PROPERLY BUT I DUNNO, LOOK INTO MORE
browser_build(){
  if [[ "${BUILD_TYPE}" == "deployment" ]]; then
    ionic build
    # kill -9 $IONIC_PID
    #python 371server-gae/main.py
  else
    # dev_appserver.py 371server-gae/main.py
    ./test_script
    # sudo du / | grep "geckodriver"
    # kill -9 $IONIC_PID # should occure after tests
  fi
}

# Builds the android version of our app.  If it's a deployment build
# does a release build and if not then builds and emulates the app for testing
# TODO: GET THE APP SIGNED W/ A KEY 
android_build(){
  ionic platform remove android
  ionic platform add android
  if [[ "${BUILD_TYPE}" == "deployment" ]]; then
    ionic build android --release
  else
    ionic build android
    ionic emulate android
  fi
}


if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
  echo 'got to build: osx'
  ios_build
elif [[ "${TRAVIS_OS_NAME}" == 'linux' ]]; then
  echo 'got to build: linux'
  export JAVA_HOME=/usr/lib/jvm/java-8-oracle
  browser_build
else
  echo 'got to build: android'
  export JAVA_HOME=/usr/lib/jvm/java-8-oracle
  android_build
fi
