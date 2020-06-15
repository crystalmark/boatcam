from gps import *
from PIL import Image
import picamera
import time
import piexif
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import json
import sys
import os
import io
from Gyro import Gyro
from Uploader import Uploader
import boto3
from paramiko import SSHClient
from scp import SCPClient
from datetime import datetime

class Position:
    def __init__(self):
        self.latitude = "Unknown"
        self.longitude = "Unknown"
        self.timestamp = "Unknown"

    def fix(self):
        gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        time.sleep(1.0)
        count = 0
        while count < 120:
            nx = gpsd.next()
            # For a list of all supported classes and fields refer to:
            # https://gpsd.gitlab.io/gpsd/gpsd_json.html
            if nx != None and nx['class'] == 'TPV':
                self.latitude = getattr(nx,'lat', "Unknown")
                self.longitude = getattr(nx,'lon', "Unknown")                
                self.timestamp = getattr(nx,'time', "Unknown")
                break
            else:
                count += 1
                time.sleep(1.0)

    def latitudeRef(self):
        if self.latitude >= 0: 
            return "N"
        else:
            return "S"

    def longitudeRef(self):
        if self.longitude >= 0:
            return "E"
        else:
            return "W"

    def absLatitude(self):
        return [int(abs(self.latitude*10000000)), 10000000]

    def absLongitude(self):
        return [int(abs(self.longitude*10000000)), 10000000]

    def toString(self):
        if self.hasFix():
            return "No fix"
        else:
            return str(self.absLatitude())+self.latitudeRef()+" "+str(self.absLongitude())+self.longitudeRef()

    def hasFix(self):
        return self.latitude == "Unknown" or self.longitude == "Unknown"

    def toJson(self):
        return {
                    'timestamp': self.timestamp,
                    'latitude': self.latitude,
                    'longitude': self.longitude
                }

class Capture:
    def __init__(self, position, voltages, filename, x_angle):
        self.position = position
        self.voltages = voltages
        self.filename = filename
        self.x_angle = x_angle

    def save(self):
        capture = {
            'timestamp': self.position.timestamp,
            'position': self.position.toJson(),
            'filename': self.filename,
            'voltages': self.voltages,
            'x': str(self.x_angle)
        }

        if not os.path.exists('capture.json'):
            capture_json = []
            with open('capture.json', 'w') as capture_file:
                json.dump(capture_json, capture_file, indent=4)
        with open('capture.json', 'r+') as capture_file:
            capture_json = json.load(capture_file)
            if capture_json == None:
                capture_json = []
            capture_json.append(capture)
            capture_file.seek(0)
            json.dump(capture_json, capture_file, indent=4)

        ssh = SSHClient()
        ssh.load_system_host_keys()
        user_name=sys.argv[1]
        web_server=sys.argv[2]
        web_server_path=sys.argv[3]
        # print (f"saving capture.json to {user_name}@{web_server}:{web_server_path}")
        ssh.connect(web_server, username=user_name)
        scp = SCPClient(ssh.get_transport())
        scp.put('capture.json', f"{web_server_path}/capture.json" )

class CaptureError:
    def __init__(self, message):
        self.message = message

class BoatImage:
    def click(self, position):
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.resolution = (1960, 1080)
            camera.rotation = 180
            camera.start_preview()
            time.sleep(2)
            camera.capture(stream, format='jpeg')
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        image = Image.open(stream)
        if image == None:
            raise CaptureError("Unable to find position")

        if position.hasFix():
            exif_bytes = self.createExif(image, position)
            return self.save(image, exif_bytes, position.timestamp)
        else:
            return self.save(image, None, datetime.today().isoformat())

    def createExif(self, image, position):
        exif_dict = piexif.load(image.info["exif"])

        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = position.latitudeRef()
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = position.absLatitude()
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = position.longitudeRef()
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = position.absLongitude()
        return piexif.dump(exif_dict)

    def save(self, image, exif_bytes, timestamp):
        new_file = "cam"+timestamp+".jpg"
        if exif_bytes != None:
            image.save(new_file, "jpeg", exif=exif_bytes)
        else:
            image.save(new_file, "jpeg")
        return new_file

def readVoltages():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan1 = AnalogIn(ads, ADS.P0)
    chan2 = AnalogIn(ads, ADS.P1)

    voltage1 = round((chan1.voltage*4.9),2)
    voltage2 = round((chan2.voltage*4.9),2)

    return {
                "voltage1": voltage1,
                "voltage2": voltage2
            }

position = Position()
position.fix()

filename = BoatImage().click(position)

voltages = readVoltages()

gyro = Gyro()
x_angle = gyro.getXDegrees()

capture = Capture(position, voltages, filename, x_angle)
capture.save()

uploader = Uploader()
uploader.upload()
