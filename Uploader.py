import logging
import glob
import os
import requests

IMAGE_URL = 'https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/'
HEADERS = {'Content-Type' : 'image/jpeg', 'x-api-key': 'kOcaoHBuT56svD7oyvEMm11PiFnQdN3L3oGFB8HL'}

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
            self.s3_client.upload_file(file_name, self.bucket_name, file_name)
            requests.post(IMAGE_URL+self.serialnumber+'/images', headers=HEADERS, files=files)
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

    def upload_json(self):
        self.upload_file("capture.json")
