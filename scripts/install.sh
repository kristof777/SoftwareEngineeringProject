#!/bin/bash
set -v

# Author: Chris Mykota-Reid ~.u 
# Installs all the packages required for whatever build is being done
# mkdir www is because Travis is a bad influence on Ionic and got it drunk
# and now needs it's hand held through the build


# downloads and installs all the files required to run ios
# you can find the versions inside the doc or posted at the end 
# of the build log
ios_install(){
  brew update
  brew cask install java
  java -version
  echo $JAVA_HOME
  npm install -g grunt-cli cordova ionic
  npm install
}

# downloads and installs all the common files required to run android/linux
# you can find the versions inside the doc or posted at the end 
# of the build log
lindroid_install(){
  sudo apt-get install oracle-java8-set-default
  npm install -g bower cordova ionic
  # installs packages specified in the ionic json
  npm install
  bower update
}

# downloads and installs all the files required to run android
# you can find the versions inside the doc or posted at the end 
# of the build log
android_install(){
  wget http://dl.google.com/android/android-sdk_r24.4-linux.tgz
  tar -xf android-sdk_r24.4-linux.tgz
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter tools-25.2.5
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter platform-tools
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter tools
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter build-tools-25.0.1
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter android-25 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-support 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-m2repository 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-google-m2repository
}

# downloads and installs google app engine for our server build
gae_install(){
  #pip list
  #curl https://sdk.cloud.google.com | bash  
  gcloud -v
  sudo gcloud components update
  echo "" | sudo gcloud components install app-engine-python
  echo "" | sudo gcloud components install app-engine-python-extras
  sudo pip install PyYAML
  sudo pip install webapp2
  sudo pip install WebOb
  ls
  ls /usr
  ls /usr/bin
  dev_appserver.py ./371server-gae/app.yaml
}


if [[ "${TRAVIS_OS_NAME}" == "osx" ]]; then
  echo "got to install osx"
  ios_install
  mkdir www
elif [[ "${TRAVIS_OS_NAME}" == "linux" ]]; then
  #echo "got to linux install"
  #lindroid_install
  gae_install
  mkdir www
else
  echo "got to install android"
  export CLOUDSDK_INSTALL_DIR=/$HOME
  export CLOUDSDK_CORE_DISABLE_PROMPTS=1
  #lindroid_install
  #android_install
  gae_install
  mkdir www
fi
