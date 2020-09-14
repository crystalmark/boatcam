import boto3
import base64
import json
import sys
import traceback
import os

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    try:
        serial_number = event["params"]["path"]["serialnumber"]
        timestamp = event["params"]["querystring"]["timestamp"]
        file_content = base64.b64decode(event['content'])

        content_object = s3.Object(os.environ['bucketName'], serial_number + '/' + timestamp + '.jpg')
        content_object.put(Body=file_content)

        return {
            "statusCode": 201,
            "headers": {'Access-Control-Allow-Origin': '*'}
        }

    except Exception as e:
        exc_info = sys.exc_info()
        stack = ''.join(traceback.format_exception(*exc_info))
        return {
            "statusCode": 200,
            "headers": {'Access-Control-Allow-Origin': '*'},
            "body": stack
        }

    return {
        "statusCode": 403,
        "headers": {'Access-Control-Allow-Origin': '*'}
    }
