#!/bin/bash

set -e

# This script should start in /app

# make a directory for the running environement
mkdir /app/unpack_dir
mkdir -p /app/runenv/validator

# unzip the submission code & find the directory that contains main
# then we copy all contents from that directory to runenv
unzip /submission/submission.zip -d /app/unpack_dir
cp -r $(dirname $(find /app/unpack_dir -name "main.py" | head -n 1))/** /app/runenv
rm -rf /app/unpack_dir/*

# unzip all validator files & find the directory that contains the validator file
# after we clean everything up
unzip /validator/validator.zip -d /app/unpack_dir
cp -r $(dirname $(find /app/unpack_dir -name "validator.py" | head -n 1))/** /app/runenv/validator
rm -rf /app/unpack_dir

# change the working directory to runenv
cd /app/runenv

# make a directory to copy the instances to
mkdir instances

# build both programs
echo "Building the submission"
chmod +x build.sh
./build.sh

echo "Building the validator"
chmod +x ./validator/build.sh
./validator/build.sh

# signal that the main code is starting
echo "Starting the main code"

for file in /instances/*; do
    # copy instance into runenv
    rm -rf /app/runenv/instances/*
    cp $file /app/runenv/instances/instance

    # create a new output folder in results
    mkdir -m 777 /results/$(basename $file)

    # run the profiler in the background
    /app/profiler.sh /results/$(basename $file)/metrics.csv &
    PROFILER_PID=$!

    # run the main code in a time wrapper, so that the statistics can be tracked
    /usr/bin/time -f "Wall time,User time,System time,Max RAM(KB)\n%e,%U,%S,%M" -o /results/$(basename $file)/CPU_times.csv python main.py

    kill $PROFILER_PID

    mv /results/results.csv /results/$(basename $file)/results.csv
done
