#!/bin/bash
if ! pgrep -f wvdial &> /dev/null 2>&1; then
  sudo usb_modeswitch -R -v 0x05c6 -p 6000
  sleep 5s
  sudo /usr/bin/wvdial &
  sleep 10s
fi
cd ~pi/boatcam
runuser -l 'pi' -c '/usr/bin/git checkout .'
runuser -l 'pi' -c '/usr/bin/git pull 2>&1'
rm -rf __pycache__
sleep 20s
sudo killall wvdial
