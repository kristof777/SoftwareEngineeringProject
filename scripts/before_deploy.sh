#!/bin/sh

# decrypts the key into github_deploy_key (maybe should but this in a more secure place)
openssl aes-256-cbc -K $encrypted_fed185e319aa_key -iv $encrypted_fed185e319aa_iv -in keys/github_deploy_key.enc -out github_deploy_key -d
# making sure the file we created has proper access rights
chmod 600 github_deploy_key
ssh-add github_deploy_key
# probably need to prep some files here
ls

# cloning the repo using ssh
# username and email should maybe should also be encrypted or at least stored in env vars
git config --global user.email "clm972@mail.usask.ca"
git config --global user.name "ChrisMykotaReid"
git remote set-url origin git@github.com:CMPT371Team1/Project.git

export PUSH_FOLDER=/home/travis/build/CMPT371Team1/Project/releases
export BUILD_FOLDER=/home/travis/build/CMPT371Team1/Project/platforms/android/build/outputs

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
git checkout master
git add $TRAVIS_BUILD_ID
git commit -m "Deploy build from $TRAVIS_BUILD_ID"
git push

