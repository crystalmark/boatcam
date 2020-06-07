#!/bin/sh
git pull
pip3 install gps3 adafruit_ads1x15
python3 capture.py
