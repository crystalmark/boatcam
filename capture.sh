#!/bin/sh
git pull
pip3 install gps adafruit_ads1x15 adafruit-blinka
python3 capture.py