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

class Position:
    def __init__(self, latitude, longitude, timestamp):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

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

def getPositionData(gps):
    count = 0
    while count < 120:
        nx = gpsd.next()
        # For a list of all supported classes and fields refer to:
        # https://gpsd.gitlab.io/gpsd/gpsd_json.html
        if nx['class'] == 'TPV':
            latitude = getattr(nx,'lat', "Unknown")
            longitude = getattr(nx,'lon', "Unknown")
            current_time = getattr(nx,'time', "Unknown")
            return Position(latitude, longitude, current_time)
        else:
            count += 1
            time.sleep(1.0)
    return None

def captureImage(picamera):
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    return Image.open(stream)   

def createExif(image, position):
    exif_dict = piexif.load(image.info["exif"])

    print (str(position.absLatitude())+position.latitudeRef()+" "+str(position.absLongitude())+position.longitudeRef())

    exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = position.latitudeRef()
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = position.absLatitude()
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = position.longitudeRef()
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = position.absLongitude()
    return piexif.dump(exif_dict)

def save(image, exif_bytes, timestamp):
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

    voltage1 = round((chan1.voltage*5),2)
    voltage2 = round((chan2.voltage*5),2)

    return {
                "voltage1": voltage1,
                "voltage2": voltage2
            }

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
time.sleep(1.0)

position = getPositionData(gpsd)
if position != None:
    print( "Your position: lon = " + str(position.longitude) + ", lat = " + str(position.latitude) )

    image = captureImage(picamera)

    if image != None:

        exif_bytes = createExif(image, position)
        #exif_bytes = None
        filename = save(image, exif_bytes, position.timestamp)
        print(filename)

        voltages = readVoltages()

        capture = {
            'timestamp': position.timestamp,
            'latitude': position.latitude,
            'longitude': position.longitude,
            'filename': filename,
            'voltages': voltages
        }
        if os.path.exists('capture.json'):
            with open('capture.json', 'r') as capture_file:
                capture_json = json.load(capture_file)
        else:
            capture_json = []
        with open('capture.json', 'w') as capture_file:
            capture_json.append(capture)
            json.dump(capture_json, capture_file, indent=4)
    else:
        print( "Not able to capture image" )
else:
    print( "No GPS position available" )
