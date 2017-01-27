#!/bin/sh

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
  # encrypting and decrypting keys goes here
  echo "should be osx"
  mkdir www
  #java -version
elif [ "$TRAVIS_OS_NAME" = "linux" ]; then
  echo "got to linux before_script"
  mkdir www
  #java -version
else
  echo "should be andriod"
  wget http://dl.google.com/android/android-sdk_r24.3.4-linux.tgz
  echo $JAVA_HOME
  tar -xvf android-sdk_r25.2.5-linux.tgz
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter platform-tools
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter build-tools-24.0.3
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter android-25
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-support
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-m2repository
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-google-m2repository
  #ls $PWD
  export ANDROID_HOME=$PWD/android-sdk-linux
  #echo $ANDROID_HOME
  mkdir www
  #java -version
  #ls /usr/lib/jvm/
  export PATH=${PATH}:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/23.0.3
fi
