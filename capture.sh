#!/bin/sh
cd ~/boatcam
git checkout .
git pull
rm -rf __pycache__
sudo service gpsd restart
sleep 2
i=0
until python3 capture.py $1 $2 $3 2>&1 >> capture.out
do
	scp capture.out *.log tim@crystalmark.co.uk:/var/www/crystalmark.co.uk/boatcam/
	((i=i+1))
	[[ i -eq 10 ]] && echo "Failed!" && exit 1
	sleep 30
	git pull
	rm -rf __pycache__
done