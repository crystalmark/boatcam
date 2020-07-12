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

    def json(self):
        return {
            'timestamp': self.position.timestamp,
            'position': self.position.to_json(),
            'filename': self.filename,
            'voltages': self.voltages,
            'x': str(self.x_angle),
            'temperature': self.temperature,
            'tide': self.tide_height,
            'disk': self.disk_usage
        }



