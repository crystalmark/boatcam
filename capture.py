import sys
from Gyro import Gyro
from Uploader import Uploader
from State import State
from Position import Position
from BoatImage import BoatImage
from Voltage import Voltages
from Tide import Tide
import os

try:
    os.system('echo "58 * * * *	~/boatcam/capture.sh boatcam" | crontab -')
except:
    print('failed to update crontab')

position = Position()
position.fix()

filename = BoatImage().click(position)

voltages = Voltages()
voltages = voltages.read_voltages()

gyro = Gyro()
x_angle = gyro.get_x_degrees()
temperature = gyro.get_temperature()

tide = Tide()
tide_height = tide.current_height()

bucket_name = sys.argv[1]
uploader = Uploader(bucket_name)

uploader.download_json()

state = State(position, voltages, filename, x_angle, temperature, tide_height)
state.save()

uploader.upload()
