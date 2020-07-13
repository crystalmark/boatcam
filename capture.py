import sys
from Gyro import Gyro
from Uploader import Uploader
from State import State
from Position import Position
from BoatImage import BoatImage
from Voltage import Voltages
from Tide import Tide
from Disk import Disk

serialnumber = sys.argv[1]

position = Position()
position.fix()

filename = BoatImage().click(position)

voltages = Voltages()
voltages = voltages.read_voltages()

gyro = Gyro()
angles = gyro.get_angles()
temperature = gyro.get_temperature()

tide = Tide()
tide_height = tide.current_height()

uploader = Uploader(serialnumber)

disk_usage = Disk.current_usage()

state = State(position, voltages, angles, temperature, tide_height, disk_usage)

print(state.json())
uploader.upload_boat_log(state.json())

print( "Uploading "+filename)
if filename is not None:
    uploader.upload_image(filename, position.timestamp)
