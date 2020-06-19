import sys
from Gyro import Gyro
from Uploader import Uploader
from State import State
from Position import Position
from BoatImage import BoatImage
from Voltage import Voltages
from Tide import Tide
from Disk import Disk
import os

bucket_name = sys.argv[1]

try:
    os.system('crontab -r')
    os.system(f"echo '0 * * * *	~/boatcam/capture.sh {bucket_name}' | crontab -")
except Exception as e:
    print('failed to update crontab')
    print(e)

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

uploader = Uploader(bucket_name)

uploader.download_json()

disk_usage = Disk.current_usage()

state = State(position, voltages, filename, x_angle, temperature, tide_height, disk_usage)
state.save()

uploader.upload_image(filename)
uploader.upload_json()
