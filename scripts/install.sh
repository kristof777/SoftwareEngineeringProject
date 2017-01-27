#!/bin/bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
  echo "got to install osx"
  #brew update
  #brew cask install java
  #java -version
  #echo $JAVA_HOME
  #npm install -g grunt-cli cordova ionic
  #npm install
elif [ "$TRAVIS_OS_NAME" = "linux" ]; then
  echo "got to linux install"
  export JAVA_HOME=/usr/lib/jvm/java-8-oracle
  npm install -g gulp bower cordova ionic
  # installs packages specified in the ionic json
  npm install
  bower update
  sudo apt-get install oracle-java8-set-default
else
  echo "got to install android"
  #export JAVA_HOME=/usr/lib/jvm/java-8-oracle
  #npm install -g gulp bower cordova ionic
  # installs packages specified in the ionic json
  #npm install
  #bower update
  #sudo apt-get install oracle-java8-set-default
fi
