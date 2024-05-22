#!/bin/bash
echo "Script loaded, starting execution"

# create a virtual environment
python3 -m venv /env
source env/bin/activate

# install the requirements
# python3 -m pip install --upgrade pip
pip install -r /code/requirements.txt

# copy the code and library to the a folder where the code will be run
cp -r /code/. /runner
cp -r /library/. /runner

# signal termination of the neworked part
echo "Execution starts. Network to be disabled."
sleep 1

# run the code
time /usr/bin/time -f "%e,%S,%U" -o /metrics/time.csv python3 /runner/main.py