#!/bin/sh

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    - brew update
    - brew cask install java
    - java -version
    - echo $JAVA_HOME
    - npm install -g grunt-cli cordova ionic
    - npm install
else
  - npm install -g gulp bower cordova ionic
  # installs packages specified in the ionic json
  - npm install
  - bower update
  - sudo apt-get install oracle-java8-set-default
fi
