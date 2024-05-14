#!/bin/bash
echo "Script loaded, starting execution"
python3 -m venv /env
source env/bin/activate
# python3 -m pip install --upgrade pip
pip install -r requirements.txt
deactivate
time /usr/bin/time -f "%e,%S,%U" -o /metrics/time.txt python3 main.py
