#!/bin/bash

# Author: Chris Mykota-Reid
# Logs into our server after a successful build using an encrypted key, and updates
# the server's repo.

set -ve

if [[ "${BUILD_TYPE}" != "deployment" ]]; then 
  SCRIPT="cd Project; git pull ; exit"

  openssl aes-256-cbc -K $encrypted_cb585f974371_key -iv $encrypted_cb585f974371_iv -in keys/server_pass.enc -out server_pass -d
  export SERVER_PASS=`cat server_pass`

  sshpass -p "${SERVER_PASS}" ssh gaa721@cmpt371g1.usask.ca "${SCRIPT}"
fi
