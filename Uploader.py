import glob
import os
import requests
import json

API_KEY = 'kOcaoHBuT56svD7oyvEMm11PiFnQdN3L3oGFB8HL'

BOATCAM_URL = 'https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/'
IMAGE_HEADERS = {'Content-Type' : 'image/jpeg', 'x-api-key': API_KEY}
LOG_HEADERS = {'Content-Type' : 'application/json', 'x-api-key': API_KEY}


class Uploader:
    def __init__(self, serialnumber):
        self.serialnumber = serialnumber

    def upload_image(self, file_name, timestamp):
        try:
            files = {'media': open(file_name, 'rb')}
            image_url = BOATCAM_URL+self.serialnumber+'/images'
            params = {'timestamp': timestamp}
            requests.post(image_url, headers=IMAGE_HEADERS, files=files, params=params)
        except requests.exceptions.RequestException as e:
            print(e)
            return False
        return True

    def upload(self):
        self.upload_images()
        self.upload_json()

    def upload_images(self):
        for file_name in glob.glob("*.jpg"):
            self.upload_file(file_name)
            os.remove(file_name)

    def upload_boat_log(self, boat_log):
        try:
            log_url = BOATCAM_URL+self.serialnumber
            requests.put(log_url, headers=LOG_HEADERS, json=boat_log)
        except requests.exceptions.RequestException as e:
            print(e)
            return False
        return True
