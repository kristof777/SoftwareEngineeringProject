#!/bin/bash

# Author: Chris Mykota-Reid
# Logs into our server after a successful build using an encrypted key, and updates
# the servers repo.

openssl aes-256-cbc -K $encrypted_cb585f974371_key -iv $encrypted_cb585f974371_iv -in server_pass.enc -out server_pass -d
export SERVER_PASS='cat server_pass'

sudo apt-get install sshpass

sshpass -p '$SERVER_PASS' ssh gaa721@cmpt371g1.usask.ca
cd Project
git pull
exit
