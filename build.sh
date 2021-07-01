#!/bin/bash

# check if sudo is used
if [ "$(id -u)" != 0 ]; then
  echo 'Sorry, you need to run this script with sudo'
  exit 1
fi

# enable I2C on Raspberry Pi
echo '>>> Enable I2C'
if grep -q 'i2c-bcm2708' /etc/modules; then
  echo 'Seems i2c-bcm2708 module already exists, skip this step.'
else
  echo 'i2c-bcm2708' >> /etc/modules
fi
if grep -q 'i2c-dev' /etc/modules; then
  echo 'Seems i2c-dev module already exists, skip this step.'
else
  echo 'i2c-dev' >> /etc/modules
fi
if grep -q 'dtparam=i2c1=on' /boot/config.txt; then
  echo 'Seems i2c1 parameter already set, skip this step.'
else
  echo 'dtparam=i2c1=on' >> /boot/config.txt
fi
if grep -q 'dtparam=i2c_arm=on' /boot/config.txt; then
  echo 'Seems i2c_arm parameter already set, skip this step.'
else
  echo 'dtparam=i2c_arm=on' >> /boot/config.txt
fi
if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
  sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
  sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
else
  echo 'File raspi-blacklist.conf does not exist, skip this step.'
fi

apt-get update

apt-get install -y git i2c-tools python3 python3-pip libjpeg-dev libtiff5 libopenjp2-7 wvdial gpsd jq

runuser -l 'pi' -c 'git clone https://github.com/crystalmark/boatcam.git'
runuser -l 'pi' -c 'cd boatcam; git checkout prototype2'
chmod a+x ~/boatcam/cmd/cmd.sh ~/boatcam/update.sh ~/boatcam/capture.sh

python3 -m pip install --upgrade pip

pip3 install smbus boto3 gps picamera piexif adafruit_blinka adafruit-circuitpython-ina219 adafruit-circuitpython-lsm9ds1 uptime


python3 -m pip install --upgrade Pillow

wget -O /etc/default/gpsd https://raw.githubusercontent.com/crystalmark/boatcam/prototype2/config/gpsd
wget -O /etc/usb_modeswitch.d/05c6:1000 https://raw.githubusercontent.com/crystalmark/boatcam/prototype2/config/05c6:1000
wget -O /etc/wvdial.conf.giffgaff https://raw.githubusercontent.com/crystalmark/boatcam/prototype2/config/wvdial.conf.giffgaff
wget -O /etc/wvdial.conf.ee https://raw.githubusercontent.com/crystalmark/boatcam/prototype2/config/wvdial.conf.ee
#wget -O /etc/udev/rules.d/49-ublox.rules https://raw.githubusercontent.com/crystalmark/boatcam/prototype2/config/49-ublox.rules
# enable camera
if grep -q 'start_x=1' /boot/config.txt; then
  echo 'Seems camera already active, skip this step.'
else
  echo 'start_x=1' >> /boot/config.txt
  echo "gpu_mem=128" >> /boot/config.txt
  echo "disable_camera_led=1" >> /boot/config.txt
  echo "dtoverlay=disable-bt" >> /boot/config.txt
fi

chmod 4754 /usr/sbin/pppd

