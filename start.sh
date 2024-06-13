#!/bin/bash

# This script should start in /app

# make a directory for the running environement
mkdir /app/unpack_dir
mkdir /app/runenv

# unzip the submission code & find the directory that contains main
# then we copy all contents from that directory to runenv
unzip /submission/submission.zip -d /app/unpack_dir
cp -r $(dirname $(find /app/unpack_dir -name "main.py" | head -n 1))/** /app/runenv
rm -rf /app/unpack_dir/*

# unzip all validator files & find the directory that contains the validator file
# after we clean everything up
unzip /validator/validator.zip -d /app/unpack_dir
cp -r $(dirname $(find /app/unpack_dir -name "validator.py" | head -n 1)) /app/runenv
rm -rf /app/unpack_dir

cd /app/runenv

pip install -r requirements.txt
pip install -r validator/requirements.txt

# run the profiler in the background
/app/profiler.sh &

# run the main code in a time wrapper, so that the statistics can be tracked
/usr/bin/time -f "Wall time,User time,System time,Max RAM(KB)\n%e,%U,%S,%M" -o /results/CPU_times.csv python main.py
