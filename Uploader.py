import logging
import boto3
from botocore.exceptions import ClientError
import glob
import os


class Uploader:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        if bucket_name is not None:
            self.bucket_name = bucket_name
        else:
            self.bucket_name = 'boatcam'

    def upload_file(self, file_name):
        try:
            self.s3_client.upload_file(file_name, self.bucket_name, file_name)
        except ClientError as e:
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
