#!/bin/bash

# run the profiler in the background

# make a directory for the running environement
mkdir runenv

# This is just for testing, use pip env in final code
pip install -r submission/requirements.txt
pip install -r validator/requirements.txt

# copy the submission and validator code to the running environment
cp -r submission/** /runenv
cp -r validator/** /runenv

# change to the running environment
cd runenv

/app/profiler.sh &
# run the main code
python main.py