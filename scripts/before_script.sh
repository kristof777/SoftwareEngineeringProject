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
  wget http://dl.google.com/android/repository/tools_r25.2.3-linux.zip
  echo $JAVA_HOME
  unzip -qq tools_r25.2.3-linux.zip
  echo y | ./tools/android update sdk --no-ui --all --filter platform-tools
  echo y | ./tools/android update sdk --no-ui --all --filter build-tools-24.0.3
  echo y | ./tools/android update sdk --no-ui --all --filter android-25
  echo y | ./tools/android update sdk --no-ui --all --filter extra-android-support
  echo y | ./tools/android update sdk --no-ui --all --filter extra-android-m2repository
  echo y | ./tools/android update sdk --no-ui --all --filter extra-google-m2repository
  cd tools
  ls 
  echo $ANDROID_HOME
  mkdir www
  #java -version
  #ls /usr/lib/jvm/
  export PATH=${PATH}:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/23.0.3
fi
