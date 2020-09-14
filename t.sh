#!/bin/sh
cd ~/boatcam
echo git pull 2>&1
i=0
until ython3 capture.py $1 $2 $3 2>&1
do
	echo "Failed to execute capture $?"
	((i=i+1))
	[[ i -eq 10 ]] && echo "Failed!" && break
	sleep 1
	echo git pull 2>&1 >> capture.out
done
echo scp /var/mail/pi tim@crystalmark.co.uk:/var/www/crystalmark.co.uk/boatcam/
