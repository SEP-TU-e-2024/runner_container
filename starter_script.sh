#!/bin/bash
echo "Script loaded, starting execution"
python3 -m venv /env
source env/bin/activate
# python3 -m pip install --upgrade pip
pip install -r requirements.txt
deactivate
python3 /scripts/timer.py 100 sleep 2
