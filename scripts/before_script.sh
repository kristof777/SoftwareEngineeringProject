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
  ./android-sdk-linux/tools/android update sdk --no-ui --all --filter platform-tools-23.0.1 
  ./android-sdk-linux/tools/android update sdk --no-ui --all --filter build-tools-24.0.3 >android_ouput.txt
  ./android-sdk-linux/tools/android update sdk --no-ui --all --filter android-24 >android_ouput.txt
  ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-support >android_ouput.txt
  ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-m2repository >android_ouput.txt
  ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-google-m2repository >android_ouput.txt
  ls 
  echo $ANDROID_HOME
  mkdir www
  #java -version
  #ls /usr/lib/jvm/
  export PATH=${PATH}:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/24.0.3
fi
