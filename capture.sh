#!/bin/sh
cd ~/boatcam
git pull
python3 capture.py $1 $2 $3