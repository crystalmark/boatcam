import glob
import os
import requests


class Uploader:

    def __init__(self, serialnumber, apikey):
        self.image_headers = {'Content-Type': 'image/jpeg', 'x-api-key': apikey}
        self.log_headers = {'Content-Type': 'application/json', 'x-api-key': apikey}
        self.url = f"https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/{serialnumber}"

    def upload_image(self, file_name, timestamp):
        try:
            image_url = f"{self.url}/images"
            params = {'timestamp': timestamp}
            # print(f"saving {file_name} to {image_url} with headers {self.image_headers}")
            response = requests.post(image_url, headers=self.image_headers, data=open(file_name, 'rb').read(), params=params)
            print(response)
        except requests.exceptions.RequestException as e:
            print(e)
        return response

    def upload(self):
        self.upload_images()
        self.upload_json()

    def upload_images(self):
        for file_name in glob.glob("*.jpg"):
            self.upload_file(file_name)
            os.remove(file_name)

    def upload_boat_log(self, boat_log):
        try:
            requests.put(f"{self.url}", headers=self.log_headers, json=boat_log)
        except requests.exceptions.RequestException as e:
            print(e)
            return False
        return True
