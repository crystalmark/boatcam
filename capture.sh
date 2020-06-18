#!/bin/bash
bucket=$1
cd ~/boatcam
[ ! -f test ] && git checkout .
[ ! -f test ] && git pull 2>&1
rm -rf __pycache__
sudo service gpsd restart
sleep 2
i=0
until python3 capture.py $bucket 2>&1 ; do
  ((i = i + 1))
  [[ i -ge 3 ]] && echo "Failed!" && break
  sleep 30
  [ ! -f test ] && git pull 2>&1
  [ ! -f test ] && rm -rf __pycache__
done
#[ ! -f test ] && aws s3 cp /var/mail/pi "s3://$bucket/pi_mail"
#[ ! -f test ] && cat /dev/null > /var/mail/pi