#!/bin/sh
cd ~/boatcam
git pull
rm -rf __pycache__
sudo service gpsd restart
python3 capture.py $1 $2 $3