#!/bin/bash

#generate a uuid and save to ~/.serialnumber
uid=`cat /proc/sys/kernel/random/uuid`
serialnumber="$(cut -d'-' -f5 <<<"$uid")"
echo $serialnumber >> ~pi/.serialnumber
echo "Serial Number: $serialnumber"

echo "Please enter the new api key for $serialnumber:"
read API_KEY
echo $API_KEY >> ~pi/.apikey

curl -s --header "Content-Type: application/json" --header "x-api-key: $API_KEY"  --request POST  https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/$serialnumber

echo "0 * * * * ~/boatcam/capture.sh $serialnumber $API_KEY > /dev/null 2>&1" | crontab -

echo '*/5-2 * * * * ~pi/boatcam/cmd/cmd.sh' | crontab -
(crontab -l 2>/dev/null; echo "@reboot [ ! -f /boot/test_flag ] && ifconfig wlan0 down") | sudo crontab -
