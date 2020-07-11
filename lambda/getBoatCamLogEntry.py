import boto3
import botocore
import json
from datetime import datetime, timedelta
import dateutil.parser
import copy
import os

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    serial_number = event["pathParameters"]["serialnumber"]
    update = json.loads(event["body"])

    try:
        content_object = s3.Object(os.environ['bucketName'], serial_number + '/log.json')
        file_content = content_object.get()['Body'].read().decode('utf-8')
        boat_log = json.loads(file_content)

        if len(boat_log["logs"]) > 0:
            log = boat_log["logs"][-1]
        else:
            log = {}

        return {
            "statusCode": 200,
            "headers": {},
            "body": log
        }
    except botocore.exceptions.ClientError as e:
        return {
            "statusCode": 404,
            "headers": {}
        }

