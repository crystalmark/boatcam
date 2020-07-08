import boto3
import botocore
import json
from datetime import datetime, timedelta
import dateutil.parser
import copy
import os

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    print(json.dumps(event))
    serial_number = event["pathParameters"]["serialnumber"]
    update = json.loads(event["body"])

    try:
        content_object = s3.Object(os.environ['bucketName'], serial_number + '/log.json')
        file_content = content_object.get()['Body'].read().decode('utf-8')
        boat_log = json.loads(file_content)

        updated_boat_log = copy.deepcopy(boat_log)
        updated_boat_log["logs"] = []

        for log in boat_log["logs"]:
            try:
                log_date = dateutil.parser.parse(log["timestamp"])
                now = datetime.now(log_date.tzinfo)
                log_age_limit = now - timedelta(days=14)
                datetime.now(log_date.tzinfo)
                if log_date > log_age_limit:
                    updated_boat_log["logs"].append(log)
            except KeyError:
                print("Ignoring log entry since it has not timestamp ")
                print(log)

        updated_boat_log["logs"].append(update)

        content_object.put(Body=json.dumps(updated_boat_log))

        return {
            "statusCode": 201,
            "headers": {}
        }
    except botocore.exceptions.ClientError as e:
        return {
            "statusCode": 404,
            "headers": {}
        }

