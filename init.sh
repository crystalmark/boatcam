#!/bin/bash

#generate a uuid and save to ~/.serialnumber
uid=`cat /proc/sys/kernel/random/uuid`
serialnumber="$(cut -d'-' -f5 <<<"$uid")"
echo $serialnumber > ~pi/.serialnumber
echo "Serial Number: $serialnumber"

apikey=$1
echo "Using $apikey:"
echo $apikey > ~pi/.apikey

curl -s --header "Content-Type: application/json" --header "x-api-key: $apikey"  --request POST  https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/$serialnumber

echo "0 * * * * ~/boatcam/capture.sh $serialnumber $apikey > /home/pi/capture.log 2>&1" | crontab -

echo '*/5-2 * * * * ~pi/boatcam/cmd/cmd.sh' | sudo crontab -
(sudo crontab -l 2>/dev/null; echo "@reboot [ ! -f /boot/test_flag ] && sleep 300 &&  ifconfig wlan0 down") | sudo crontab -

jq -n --arg serialnumber "$serialnumber" --arg apikey "$apikey" '{serialnumber: $serialnumber, apikey: $apikey, rolloffset: 0, pitchoffset: 180, voltage1: { name: "Leisure Battery", connection: 1, critial: 10.5, warn: 11.2, full: 14.2 }, voltage2: { name: "Engine Battery", connection: 2, critial: 10.5, warn: 11.2, full: 14.2 }}' > ~pi/settings.json

