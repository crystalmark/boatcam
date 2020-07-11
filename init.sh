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

# install i2c-tools
echo '>>> Install i2c-tools'
if hash i2cget 2>/dev/null; then
  echo 'Seems i2c-tools is installed already, skip this step.'
else
  apt-get install -y i2c-tools
fi

apt-get install -y git

apt-get install -y python3 python3-pip

runuser -l 'pi' -c 'git clone https://github.com/crystalmark/boatcam.git'
runuser -l 'pi' -c 'cd boatcam; git checkout prototype1'

pip3 install smbus boto3 gps picamera piexif board adafruit-circuitpython-ina219 adafruit-circuitpython-lsm9ds1

apt-get install -y libjpeg-dev

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

apt-get install -y gpsd

wget -O /etc/default/gpsd https://raw.githubusercontent.com/crystalmark/boatcam/prototype1/config/gpsd

#generate a uuid and save to ~/.serialnumber
uid=`cat /proc/sys/kernel/random/uuid`
serialnumber="$(cut -d'-' -f5 <<<"$uid")"
echo $serialnumber >> ~pi/.serialnumber
echo "Serial Number: $serialnumber"

curl -s --header "Content-Type: application/json" --header "x-api-key: $1"  --request POST  https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/$serialnumber

echo $API_KEY >> ~pi/.apikey

runuser -l 'pi' -c 'echo "0 * * * * ~/boatcam/capture.sh boatcam $API_KEY > /dev/null 2>&1" | crontab -'

# enable camera
echo "start_x=1" >> /boot/config.txt
echo "gpu_mem=128" >> /boot/config.txt
echo "disable_camera_led=1" >> /boot/config.txt


