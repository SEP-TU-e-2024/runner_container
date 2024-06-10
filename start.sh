#!/bin/bash

# run the profiler in the background
profiler.sh &

# make a directory for the running environement
mkdir runenv
mkdir unpack_dir

# unzip the submission code & find the directory that contains main
# then we copy all contents from that directory to runenv
unzip submission/submission.zip -d unpack_dir
cp -r $(dirname $(find /unpack_dir -name "main.py" | head -n 1))/** /runenv
rm -rf /unpack_dir/*

# unzip all validator files & find the directory that contains the validator file
# after we clean everything up
unzip validator/validator.zip -d -o unpack_dir
cp -r $(dirname $(find /unpack_dir -name "validator.py" | head -n 1)) /runenv
rm -rf /unpack_dir

cd /runenv
pipenv shell

pipenv install -r requirements.txt
pipenv install -r validator/requirements.txt

# run the main code
python main.py