#!/bin/bash

# Author: Chris Mykota-Reid
# Logs into our server after a successful build using an encrypted key, and updates
# the servers repo.

openssl aes-256-cbc -K $encrypted_cb585f974371_key -iv $encrypted_cb585f974371_iv -in keys/server_key.enc -out server_key -d
chmod 600 server_key
eval "$(ssh-agent -s)"
ssh-add server_key 

if [[ -z "ssh-keygen -F cmpt371g1.usask.ca" ]]; then
  ssh-keyscan -H cmpt371g1.usask.ca >> ~/.ssh/known_hosts
fi

ssh -q gaa721@cmpt371g1.usask.ca
cd Project
git pull
exit
