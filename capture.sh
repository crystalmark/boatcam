#!/bin/sh
cd ~/boatcam
git pull
rm -rf __pycache__
python3 capture.py $1 $2 $3