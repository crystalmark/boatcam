import boto3
import botocore
import json
import os

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    serial_number = event["pathParameters"]["serialnumber"]

    try:
        content_object = s3.Object(os.environ['bucketName'], serial_number + '/log.json')

        boat_log = {
            "serialNumber": serial_number,
            "apiKey": "TODO",
            "telephone": {
                "number": "TODO",
                "supplier": "TODO"
            },
            "logs": []
        }
        content_object.put(Body=json.dumps(boat_log))

        return {
            "statusCode": 201,
            "headers": {},
            "body": json.dumps(boat_log)
        }
    except botocore.exceptions.ClientError as e:
        return {
            "statusCode": 500,
            "headers": {},
            "body": e
        }

