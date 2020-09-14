import boto3
from botocore.exceptions import ClientError
import base64
import os

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    try:
        serial_number = event["params"]["path"]["serialnumber"]
        timestamp = event["params"]["path"]["timestamp"]

        content_object = s3.Object(os.environ['bucketName'], serial_number + '/' + timestamp + '.jpg')
        file_content = content_object.get()

        return {
            "statusCode": 200,
            "headers": {'Access-Control-Allow-Origin': '*', 'Content-Type': 'image/jpeg'},
            "body": base64.encode(file_content)
        }

    except ClientError:
        return {
            "statusCode": 404
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": {'Access-Control-Allow-Origin': '*'}
        }

    return {
        "statusCode": 403,
        "headers": {'Access-Control-Allow-Origin': '*'}
    }
