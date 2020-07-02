import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219


class Voltages:
    def __init__(self):
        try:
            i2c_bus = board.I2C()

            self.chan1 = INA219(i2c_bus, addr=0x40)
            self.chan2 = INA219(i2c_bus, addr=0x41)

            self.chan1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan1.bus_voltage_range = BusVoltageRange.RANGE_16V

            self.chan2.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan2.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan2.bus_voltage_range = BusVoltageRange.RANGE_16V
        except:
            print("No voltage monitor connected")
            self.chan1 = None
            self.chan2 = None

    def read_voltages(self):

        if self.chan1 is not None:
            voltage1 = round(self.chan1.shunt_voltage, 2)
            voltage1 = round(self.chan2.shunt_voltage, 2)
        else:
            voltage1 = None
            voltage2 = None

        return {
            "voltage1": voltage1,
            "voltage2": voltage2
        }

