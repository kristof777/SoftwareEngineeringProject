#!/bin/sh

# probably need to prep some files here
export PUSH_FOLDER=/home/travis/build/CMPT371Team1/Project/releases
export BUILD_FOLDER=/home/travis/build/CMPT371Team1/Project/platforms/android/build/outputs

openssl aes-256-cbc -K $encrypted_fed185e319aa_key -iv
$encrypted_fed185e319aa_iv -in github_deploy_key.enc -out github_deploy_key -d

# Create folder to deploy to
cd $PUSH_FOLDER
mkdir $TRAVIS_BUILD_ID
cd $TRAVIS_BUILD_ID

# move deployment files to the folder we are going to push
cp -r $BUILD_FOLDER $PUSH_FOLDER/$TRAVIS_BUILD_ID
ls
cd ..
ls

# push it to git!
git config --global push.default matching
git config --global user.email "clm972@mail.usask.ca"
git config --global user.name "ChrisMykotaReid"

git checkout master
git add $TRAVIS_BUILD_ID
git commit -m "Deploy build from $TRAVIS_BUILD_ID"
git push
