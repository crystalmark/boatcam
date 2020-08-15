from TextMessageRetriever import TextMessageRetriever
from TextMessage import TextMessage
import subprocess
import sys
from datetime import datetime

def clean(s):
    return s.strip('"').strip("'").lower().strip()


def run(task, sender, number):
    try:
        print(f"executing command {task}")
        result = subprocess.check_output(task, shell=True)
        sender.send_message(number, f"executed command: {task}")
        print(result)
    except subprocess.CalledProcessError as e:
        sender.send(number, f"failed to execute command: {task}")
        print(e)


serialnumber = sys.argv[1]
apikey = sys.argv[2]

print(datetime.now())

receiver = TextMessageRetriever(debug=True)
receiver.connect_phone()
m=receiver.read_sms()
receiver.delete_read_sms()
receiver.disconnect_phone()
if len(m) > 1:
    number_of_messages = int(len(m)/2)
    print(f"Number of messages: {number_of_messages}")
    for x in range(0, number_of_messages):
        print(f"parsing message {x+1}")
        meta = m[x*2].split(',')
        message = clean(m[(x*2)+1])
        tm = TextMessage(phone=clean(meta[2]), received=f"{clean(meta[4])} {clean(meta[5])}", message=clean(message))
        print(tm.to_string())

        if tm.message.startswith(f"cmd {serialnumber}"):
            cmd = tm.message.replace(f"cmd {serialnumber} ", "")
            if cmd == 'wifi off':
                run("/sbin/ifconfig wlan0 down", receiver, tm.phone)
            elif cmd == 'wifi on':
                run("/sbin/ifconfig wlan0 up", receiver, tm.phone)
            elif cmd == 'now':
                run(f"/home/pi/boatcam/capture.sh {serialnumber} {apikey}", receiver, tm.phone)
            elif cmd == 'update':
                run("/home/pi/boatcam/update.sh", receiver, tm.phone)
            elif cmd == 'reboot':
                run("/sbin/reboot", receiver, tm.phone)
            elif cmd == 'shutdown':
                run("/sbin/shutdown -h now", receiver, tm.phone)
            else:
                print(f"Not a valid command: {tm.message}")
                receiver.send_message(tm.phone, f"command not recognised: {tm.message}")
        else:
            receiver.send_message(tm.phone, f"not a valid command: {tm.message}")
            print(f"Not a valid command: {tm.message}")
else:
    print("No messages")
