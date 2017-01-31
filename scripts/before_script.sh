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
  wget http://dl.google.com/android/android-sdk_r24.4-linux.tgz
  echo $JAVA_HOME
  tar -xf android-sdk_r24.4-linux.tgz
  
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter tools-25.2.5
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter platform-tools
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter tools
 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter build-tools-25.0.1
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter android-25 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-support 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-m2repository 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-google-m2repository
  ls 
  echo $PWD
  echo $ANDROID_HOME
  mkdir www
  #java -version
  #ls /usr/lib/jvm/
fi
