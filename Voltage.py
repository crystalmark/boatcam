import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219


class Voltages:
    def __init__(self):
        try:
            i2c_bus = board.I2C()

            self.chan1 = INA219(i2c_bus, addr=0x40)
            self.chan2 = INA219(i2c_bus, addr=0x41)
            self.chan3 = INA219(i2c_bus, addr=0x42)
            self.chan4 = INA219(i2c_bus, addr=0x43)

            self.chan1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan1.bus_voltage_range = BusVoltageRange.RANGE_16V

            self.chan2.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan2.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan2.bus_voltage_range = BusVoltageRange.RANGE_16V

            self.chan3.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan3.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan3.bus_voltage_range = BusVoltageRange.RANGE_16V

            self.chan4.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan4.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.chan4.bus_voltage_range = BusVoltageRange.RANGE_16V
        except:
            print("No voltage monitor connected")
            self.chan1 = None
            self.chan2 = None
            self.chan3 = None
            self.chan4 = None

    def read_voltages(self):

        if self.chan1 is not None:
            voltage1 = round(self.chan1.bus_voltage, 2)
        else:
            voltage1 = None
        if self.chan2 is not None:
            voltage2 = round(self.chan2.bus_voltage, 2)
        else:
            voltage2 = None
        if self.chan3 is not None:
            voltage3 = round(self.chan3.bus_voltage, 2)
        else:
            voltage3 = None
        if self.chan4 is not None:
            voltage4 = round(self.chan4.bus_voltage, 2)
        else:
            voltage4 = None

        return {
            "voltage1": voltage1,
            "voltage2": voltage2,
            "voltage3": voltage3,
            "voltage4": voltage4
        }

