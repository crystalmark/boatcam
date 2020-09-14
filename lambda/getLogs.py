import boto3
import botocore
import json
from datetime import datetime, timedelta

s3 = boto3.resource('s3')

numdays = 14


def latest_logs(logs):
    a = datetime.today().replace(minute=0, second=0, microsecond=0)
    a = a - timedelta(days=numdays)
    dates = []
    for day in range (0, numdays):
        for hour in range(0, 24):
            dates.append(a + timedelta(hours=(day*24)+hour))

    logs_latest = []
    for timestamp in dates:
        start = timestamp - timedelta(hours=6)
        end = timestamp + timedelta(hours=6)
        log_latest = None
        for log in logs:
            try:
                log_time = datetime.strptime(log['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                log_time = datetime.strptime(log['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
            if start < log_time < end:
                log_latest = log.copy()
                log_latest['timestamp'] = f"{str(timestamp)}"
        if log_latest is not None:
            logs_latest.append(log_latest)
        else:
            logs_latest.append({"timestamp": f"{str(timestamp)}"})

    return logs_latest


def lambda_handler(event, context):
    print(json.dumps(event))
    serial_number = event["pathParameters"]["serialnumber"]

    try:
        content_object = s3.Object("boatcamtest", serial_number + '/log.json')
        file_content = content_object.get()['Body'].read().decode('utf-8')
        boat_log = json.loads(file_content)

        logs = boat_log["logs"]


        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(latest_logs(logs),default=str)
        }
    except botocore.exceptions.ClientError as e:
        return {
            "statusCode": 404,
            "headers": {}
        }

