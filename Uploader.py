import logging
import boto3
from botocore.exceptions import ClientError
import glob
import os

class Uploader():
    bucket = 'boatcam'
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def upload_file(self, file_name):
        try:
            response = self.s3_client.upload_file(file_name, self.bucket, file_name)
        except ClientError as e:
            logging.error(e)
            return False
        os.remove(file_name)
        return True

    def upload(self):
        for file_name in glob.glob("*.jpg"):
            self.upload_file(file_name)
