#!/bin/sh
cd ~/boatcam
sudo pip3 install suntime
git checkout .
git pull
rm -rf __pycache__
sudo service gpsd restart
sleep 2
python3 capture.py $1 $2 $3