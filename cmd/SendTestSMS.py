from TextMessageRetriever import TextMessageRetriever
import sys
import os

with open(os.path.expanduser("~/.serialnumber"), 'r') as f:
    serialnumber = f.readline()
    tm = TextMessageRetriever(debug=True)
    tm.connect_phone()
    tm.send_message(content=f"Hello from the BoatCam :-) Serial number: {serialnumber}", recipient=sys.argv[1])
    tm.disconnect_phone()
