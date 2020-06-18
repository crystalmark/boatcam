import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import sys
from Gyro import Gyro
from Uploader import Uploader
from State import State
from Position import Position
from BoatImage import BoatImage

VOLTAGE_RATIO = 4.9


class Voltages:
    def __init__(self):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ADS.ADS1115(i2c)
            self.chan1 = AnalogIn(ads, ADS.P0)
            self.chan2 = AnalogIn(ads, ADS.P1)
        except:
            print("No voltage monitor connected")
            self.chan1 = None
            self.chan2 = None

    def read_voltages(self):

        if self.chan1 is not None:
            voltage1 = round((self.chan1.voltage * VOLTAGE_RATIO), 2)
            voltage2 = round((self.chan2.voltage * VOLTAGE_RATIO), 2)
        else:
            voltage1 = None
            voltage2 = None

        return {
            "voltage1": voltage1,
            "voltage2": voltage2
        }

