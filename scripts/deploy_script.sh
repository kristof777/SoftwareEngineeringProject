#!/bin/bash

# Author: Chris Mykota-Reid
# Does everything related to the deployment of a release.  Sets up ssh keys
# , gets us checked out onto the right branch and security type for git,
# gets files prepped for deployment, and lastly deploys them



# un-encrypts the ssh key, starts up adds it to the list of keys
setup_ssh(){
  openssl aes-256-cbc -K $encrypted_fed185e319aa_key -iv $encrypted_fed185e319aa_iv -in keys/github_deploy_key.enc -out github_deploy_key -d
  chmod 600 github_deploy_key
  eval "$(ssh-agent -s)"
  ssh-add github_deploy_key
}

# sets email and username to the person who the ssh key is linked to, 
# changes the url to the ssh one (initially repo is cloned using https)
# then checks out which ever branch we are doing the release for
# (currently hard coded to develop)
setup_git(){
  git config --global user.email "clm972@mail.usask.ca"
  git config --global user.name "ChrisMykotaReid"
  git remote set-url origin git@github.com:CMPT371Team1/Project.git
  git checkout develop
}

# sets up the Travis environment for deployment by making the dir for the particular release
# then copying the files for deployment into it
setup_deploy(){
  cd ${PUSH_FOLDER}
  mkdir ${TRAVIS_BUILD_ID}
  cd ${TRAVIS_BUILD_ID}
  cp -r ${BUILD_FOLDER} ${PUSH_FOLDER}/${TRAVIS_BUILD_ID}
}

# moves compiled files to the right repo folder then pushes the files to the repo
# this should be changed to run some kind of releases script
deploy(){
  git add ${TRAVIS_BUILD_ID}
  git commit -m "Deploy build from $TRAVIS_BUILD_ID [ci skip]"
  git push
}


if [[ "${BUILD_TYPE}" == "deployment" ]]; then
  setup_ssh()
  setup_git()

  export PUSH_FOLDER=/home/travis/build/CMPT371Team1/Project/releases
  export BUILD_FOLDER=/home/travis/build/CMPT371Team1/Project/platforms/android/build/outputs

  setup_deploy()
  deploy()
else
  echo "Not deploying because this isn't a deployment build"
fi
