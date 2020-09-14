#!/usr/bin/env python

import requests
import shutil
import time
import sys
import logging

logger = logging.getLogger('360')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('360.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

time.sleep(5.0)

BASEURL = 'http://192.168.107.1/osc/'

resp = requests.get(BASEURL + 'info')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /osc/info/ {}'.format(resp.status_code))

logger.info('Manufacturer: {}'.format(resp.json()["manufacturer"]))
logger.info('Model: {}'.format(resp.json()["model"]))
logger.info('Firmware: {}'.format(resp.json()["firmwareVersion"]))
logger.info('Serial: {}'.format(resp.json()["serialNumber"]))
logger.info(resp)
logger.info(resp.json())


resp = requests.post(BASEURL + 'state')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /osc/state/ {}'.format(resp.status_code))

logger.info('batteryLevel: {}'.format(resp.json()["state"]["batteryLevel"]*100))

data = {"name": "camera.startSession", "parameters": {} }

resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('camera.startSession: {}'.format(resp.status_code))


sessionId = (resp.json()["results"]["sessionId"])
logger.info('SessionId: {}'.format(sessionId))

# TAKE A NEW IMAGE

logger.info('Say cheese!')

data = {"name": "camera.takePicture", "parameters": { "sessionId": sessionId} }
resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('camera.takePicture: {}'.format(resp.status_code))
pictureId = (resp.json()["id"])

logger.info('Click!')

# WAIT FOR LAST IMAGE TO CHANGE

sys.stdout.write('Waiting for image processing')
sys.stdout.flush()

for x in range(1, 30):
    sys.stdout.write('.')
    sys.stdout.flush()
    data = {"id": pictureId } 
    resp = requests.post(BASEURL + 'commands/status', json=data)
    if format(resp.json()["state"])=='done': 
        break
    time.sleep(0.5)

logger.info('')
uri = resp.json()["results"]["fileUri"]
#logger.info('uri: {}'.format(uri))



# GET NEW IMAGE

name="OSC_" + pictureId+".JPG"

data = {"name": "camera.getImage", "parameters": { "fileUri": uri} }

resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('camera.getImage: {}'.format(resp))


# SAVE NEW IMAGE

resp.raw.decode_content = True

with open(name,'wb') as ofh:
    for chunk in resp:
            ofh.write(chunk)
        
logger.info('Image stored as: {}'.format(name))