#!/bin/bash
openssl aes-256-cbc -K $encrypted_cb585f974371_key -iv $encrypted_cb585f974371_iv -in server_key.enc -out server_key -d
