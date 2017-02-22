#!/bin/bash

# Author: Chris Mykota-Reid :>
# This script calls the commands required to compile (TODO: TESTING)
# and emulate our program

set v

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
    ionic platform remove ios
    ionic build
    # kill -9 $IONIC_PID
    ls
    #python 371server-gae/main.py
  else
    # dev_appserver.py 371server-gae/main.py
    screen -d -m -L ionic serve --firefox@47.0.1
    sleep 50
    # sudo du / | grep "geckodriver"
    # webdriver-manager start &
    protractor e2e-tests.conf.js --troubleshoot 
    # kill -9 $IONIC_PID # should occure after tests
    echo "${PYTHONPATH}"
    ls
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

# Displays versions of the main: sdks, tools and platforms used for the build
system_info(){
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
  #ionic info
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
system_info
