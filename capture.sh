#!/bin/sh
cd ~/boatcam
git checkout .
git pull 2>&1 > capture.out
rm -rf __pycache__
sudo service gpsd restart
sleep 2
i=0
until [[ i -eq 10 ]] && python3 capture.py $1 $2 $3 2>&1 >> capture.out
do
	echo "Failed to execute capture $?" >> capture.out
	scp capture.out tim@crystalmark.co.uk:/var/www/crystalmark.co.uk/boatcam/
	((i=i+1))
	sleep 30
	git pull 2>&1 >> capture.out
	rm -rf __pycache__
done
scp /var/mail/pi tim@crystalmark.co.uk:/var/www/crystalmark.co.uk/boatcam/