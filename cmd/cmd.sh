#!/bin/bash

serialnumber=$(<~pi/.serialnumber)
apikey=$(<~pi/.apikey)

date

n=0
until [ "$n" -ge 3 ]
do
  if ! pgrep -f wvdial &> /dev/null 2>&1; then
    cd ~pi/boatcam/cmd/
  #  python3 RetrieveSMS.py $serialnumber >> /dev/null 2>> ~pi/cmd.log
    python3 RetrieveSMS.py $serialnumber $apikey >> ~pi/cmd.log 2>&1
    break;
  else
    ((n=n+1))
    echo wvial is running so cannot connect to the modem $n >> ~pi/cmd.log 2>&1
    sleep 1m
  fi
done
