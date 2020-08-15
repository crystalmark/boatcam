#!/bin/bash
serialnumber=$1
apikey=$2
. ~/.profile

/bin/date

if ! /usr/bin/pgrep -f wvdial &> /dev/null 2>&1; then
#  sudo usb_modeswitch -R -v 0x05c6 -p 6000
  sleep 5s
  sudo /usr/bin/wvdial &
  sleep 30s
else
  echo wvdial is already running
fi
cd ~pi/boatcam
rm -f ./*.jpg
i=0
until python3 capture.py $serialnumber $apikey 2>&1 ; do
  ((i = i + 1))
  [[ i -ge 3 ]] && echo "Failed more than 3 times!" && break
  sleep 30
  if ! /usr/bin/pgrep -f wvdial &> /dev/null 2>&1; then
#    sudo usb_modeswitch -R -v 0x05c6 -p 6000
    sleep 5s
    sudo /usr/bin/wvdial &
    sleep 30s
  fi
done
sleep 20s
sudo killall wvdial
