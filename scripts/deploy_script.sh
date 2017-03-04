#!/bin/bash

# Author: Chris Mykota-Reid
# Does everything related to the deployment of a release.  Sets up ssh keys
# , gets us checked out onto the right branch and security type for git,
# gets files prepped for deployment, and lastly deploys them



# Un-encrypts the ssh key, starts up the ssh agent and adds it to the list of keys on the
# Travis machine.
setup_ssh(){
  openssl aes-256-cbc -K $encrypted_fed185e319aa_key -iv $encrypted_fed185e319aa_iv -in keys/github_deploy_key.enc -out github_deploy_key -d
  chmod 600 github_deploy_key
  eval "$(ssh-agent -s)"
  ssh-add github_deploy_key
}

# Sets the git email and username to the person who the ssh key is linked to. 
# Changes the url to the ssh one (initially repo is cloned using https),
# then checks out which ever branch we are doing the release for
setup_git(){
  git config --global user.email "clm972@mail.usask.ca"
  git config --global user.name "ChrisMykotaReid"
  git remote set-url origin git@github.com:CMPT371Team1/Project.git
  git checkout develop
}

# Sets up the Travis environment for deployment by making the dir for the particular release,
# then copying the files for deployment into it.
setup_deploy(){
  cd ${PUSH_FOLDER}
  mkdir "${TRAVIS_BUILD_ID}"
  cd ${TRAVIS_BUILD_ID}
  cp -r ${BUILD_FOLDER} ${PUSH_FOLDER}/${TRAVIS_BUILD_ID}
  cd ${TRAVIS_BUILD_ID}
  ls 
  cd ..
}

# Moves the compiled files to the right folder then pushes the files to the repo.
# TODO Figure out Github releases using a script.
# This should be changed to run some kind of releases script.
deploy(){
  git add ${TRAVIS_BUILD_ID}
  git commit -m "Deploy build from $TRAVIS_BUILD_ID [ci skip]"
  git push
}


if [[ "${BUILD_TYPE}" == "deployment" ]]; then
  setup_ssh
  setup_git

  # variables used for
  export PUSH_FOLDER=/home/travis/build/CMPT371Team1/Project/releases
  export BUILD_FOLDER=/home/travis/build/CMPT371Team1/Project/platforms/android/build/outputs

  setup_deploy
  deploy
else
  echo "Not deploying because this isn't a deployment build"
fi
