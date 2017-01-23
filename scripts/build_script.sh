#!/bin/bash

if [[ $TRAVIS_OS_NAME = 'osx' ]]; then
  ionic platform add ios
  ionic build
else
  ionic platform remove andriod
  ionic platform add andriod
  ionic build
fi
