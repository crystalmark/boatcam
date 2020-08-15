class State:
    def __init__(self, position, voltages, angles, temperature, tide_height, disk_usage, uptime):
        self.position = position
        self.voltages = voltages
        self.angles = angles
        self.temperature = temperature
        self.tide_height = tide_height
        self.disk_usage = disk_usage
        self.uptime = uptime

    def json(self):
        return {
            'timestamp': self.position.timestamp,
            'position': self.position.to_json(),
            'voltages': self.voltages,
            'angles': self.angles,
            'temperature': self.temperature,
            'tide': self.tide_height,
            'disk': self.disk_usage,
            'uptime': self.uptime
        }



