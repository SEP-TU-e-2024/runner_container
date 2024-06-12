#!/bin/bash

# make a directory for the running environement
mkdir runenv

# This is just for testing, use pip env in final code
pip install -r submission/requirements.txt
pip install -r validator/requirements.txt

# copy the submission and validator code to the running environment
cp -r submission/** ./runenv
cp -r validator/** ./runenv

# change to the running environment
cd runenv

# run the profiler in the background
/app/profiler.sh &

# run the main code in a time wrapper, so that the statistics can be tracked
/usr/bin/time -f "Wall time,User time,System time,User child time,System child time,Max RAM\n%e,%U,%S,%u,%s,%M" -o /results/CPU_times.csv python main.py