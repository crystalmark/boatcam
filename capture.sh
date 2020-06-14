#!/bin/sh
cd ~/boatcam
git checkout .
git pull
rm -rf __pycache__
rm -f capture.json
sudo service gpsd restart
sleep 2
python3 capture.py $1 $2 $3