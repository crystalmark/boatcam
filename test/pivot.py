import json
from datetime import datetime, timedelta

numdays = 7


def latest_logs(logs):
    a = datetime.today().replace(minute=0, second=0, microsecond=0)
    a = a - timedelta(days=numdays)
    dates = []
    for day in range(0, numdays):
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


with open("capture.json", 'r') as f:
    logs = json.load(f)
    latest = latest_logs(logs)
    print(json.dumps(latest,default=str))


