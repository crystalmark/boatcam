from gps import *
import time


class Position:
    def __init__(self):
        self.latitude = "Unknown"
        self.longitude = "Unknown"
        self.timestamp = "Unknown"

    def fix(self):
        gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        time.sleep(1.0)
        count = 0
        while count < 120:
            nx = gpsd.next()
            # For a list of all supported classes and fields refer to:
            # https://gpsd.gitlab.io/gpsd/gpsd_json.html
            if nx is not None and nx['class'] == 'TPV':
                self.latitude = getattr(nx, 'lat', "Unknown")
                self.longitude = getattr(nx, 'lon', "Unknown")
                self.timestamp = getattr(nx, 'time', "Unknown")
                break
            else:
                count += 1
                time.sleep(1.0)

    def latitude_ref(self):
        if self.latitude >= 0:
            return "N"
        else:
            return "S"

    def longitude_ref(self):
        if self.longitude >= 0:
            return "E"
        else:
            return "W"

    def abs_latitude(self):
        return [int(abs(self.latitude * 10000000)), 10000000]

    def abs_longitude(self):
        return [int(abs(self.longitude * 10000000)), 10000000]

    def to_string(self):
        if self.has_fix():
            return "No fix"
        else:
            return str(self.abs_latitude()) + self.latitude_ref() + " " + str(
                self.abs_longitude()) + self.longitude_ref()

    def has_fix(self):
        return self.latitude is not None and self.longitude is not None and self.latitude != "Unknown" and self.longitude != "Unknown"

    def to_json(self):
        return {
            'timestamp': self.timestamp,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

