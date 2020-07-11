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

        content_object = s3.Object(os.environ['bucketName'], serial_number + '/log.json')
        file_content = content_object.get()['Body'].read().decode('utf-8')
        boat_log = json.loads(file_content)

        if len(boat_log["logs"]) > 0:
            timestamp = boat_log["logs"][-1]["timestamp"]
            content_object = s3.Object(os.environ['bucketName'], serial_number + '/' + timestamp + '.jpg')
            return {
                "statusCode": 200,
                "body": content_object.get()['Body'].read()
            }
            {
                "isBase64Encoded": True,
                "statusCode": 200,
                "headers": {"content-type": "image/jpg"},
                "body": base64.b64encode(content_bytes).decode("utf-8")
            }
        else:
            return {
                "statusCode": 200
            }

    except Exception as e:
        exc_info = sys.exc_info()
        stack = ''.join(traceback.format_exception(*exc_info))
        return {
            "statusCode": 200,
            "headers": {'Access-Control-Allow-Origin': '*'},
            "body": json.dumps(event)
        }

    return {
        "statusCode": 403,
        "headers": {'Access-Control-Allow-Origin': '*'}
    }

