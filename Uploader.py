import logging
import glob
import os
import requests

API_KEY = 'kOcaoHBuT56svD7oyvEMm11PiFnQdN3L3oGFB8HL'

BOATCAM_URL = 'https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/'
IMAGE_HEADERS = {'Content-Type' : 'image/jpeg', 'x-api-key': API_KEY}
LOG_HEADERS = {'Content-Type' : 'application/json', 'x-api-key': API_KEY}


class Uploader:
    def __init__(self, bucket_name, serialnumber):
        if bucket_name is not None:
            self.bucket_name = bucket_name
        else:
            self.bucket_name = 'boatcam'
        self.serialnumber = serialnumber

    def upload_image(self, file_name):
        try:
            files = {'media': open(file_name, 'rb')}
            requests.post(BOATCAM_URL+self.serialnumber+'/images', headers=IMAGE_HEADERS, files=files)
        except requests.exceptions.RequestException as e:
            logging.error(e)
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
            requests.put(BOATCAM_URL+self.serialnumber, headers=LOG_HEADERS, json=boat_log)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return False
        return True
