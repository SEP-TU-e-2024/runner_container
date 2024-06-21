#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Use './run.sh <problem name>'"
	exit 1
fi

cd $1

# Zip the submission
echo "Creating submission.zip"
cd submission
rm ../submission.zip
zip -r ../submission.zip ./*
cd ..

# Zip the validator
echo "Creating validator.zip"
cd validator
rm ../validator.zip
zip -r ../validator.zip ./*
zip -j ../validator.zip ../../IOModule.py
cd ..

# Start the web server
python3 -m http.server 8001
