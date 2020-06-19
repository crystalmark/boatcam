import json
import os


class State:
    def __init__(self, position, voltages, filename, x_angle, temperature, tide_height, disk_usage):
        self.position = position
        self.voltages = voltages
        self.filename = filename
        self.x_angle = x_angle
        self.temperature = temperature
        self.tide_height = tide_height
        self.disk_usage = disk_usage

    def save(self):
        capture = {
            'timestamp': self.position.timestamp,
            'position': self.position.to_json(),
            'filename': self.filename,
            'voltages': self.voltages,
            'x': str(self.x_angle),
            'temperature': self.temperature,
            'tide': self.tide_height,
            'disk': self.disk_usage
        }

        if not os.path.exists('capture.json'):
            capture_json = []
            with open('capture.json', 'w') as capture_file:
                json.dump(capture_json, capture_file, indent=4)
        with open('capture.json', 'r+') as capture_file:
            capture_json = json.load(capture_file)
            if capture_json is None:
                capture_json = []
            capture_json.append(capture)
            capture_file.seek(0)
            json.dump(capture_json, capture_file, indent=4)



