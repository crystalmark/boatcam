import serial
import time
import re

SERVICE_PROVIDERS = [
#    MCC+MNC, CSCA,            init1, init2,                               init3,                              username,   password,    name
    ['23410', '+447802002606', 'ATZ', 'ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0', 'AT+CGDCONT=1,"IP","giffgaff.com"', 'giffgaff', 'password', 'GiffGaff'],
    ['23430', '+447958879879', 'ATZ', 'ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0', 'AT+CGDCONT=1,"IP","everywhere"',   None,       None,        'EE'],
    ['23431', '+447958879879', 'ATZ', 'ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0', 'AT+CGDCONT=1,"IP","everywhere"',   None,       None,        'EE'],
    ['23432', '+447958879879', 'ATZ', 'ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0', 'AT+CGDCONT=1,"IP","everywhere"',   None,       None,        'EE']
]


class ConnectioError:
    def __init__(self, message):
        self.message = message


class TextMessageRetriever:
    def __init__(self, debug=False):
        self.ser = None
        self.debug = debug

    def log(self, message):
        if self.debug:
            print(message)

    def get_CSCA_number(self):
        id = self.write('AT+CIMI')
        self.log(f"Looking for CSCA number in {str(id)}")
        for supplier in SERVICE_PROVIDERS:
            if id[0].startswith(f"+CIMI:{supplier[0]}"):
                self.log(f"Using service provider {supplier[7]}")
                return supplier[1]
        return None

    def connect_phone(self):
        self.log("connecting to phone")
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)
        time.sleep(0.5)
        self.ser = self.reset_modem()
        self.log(str(self.write('AT+CLAC?')))
        self.log(str(self.write('AT+CREG=1')))
        self.log(str(self.write('AT+CREG?')))
        self.write('AT+CSCA="' + self.get_CSCA_number() + '"')

    def write(self, message, wait=1):
        if self.ser is None:
            self.connect_phone()
        self.log(message)
        m = message + '\r\n'
        self.log(f"clearing responses: {self.read()}")
        self.ser.write(m.encode())
        time.sleep(wait)
        return self.read()

    def send_message(self, recipient, content):
        if len(recipient) < 15:
            self.write('AT+CMGF=1')
            self.write('''AT+CMGS="''' + recipient + '''"''')
            self.write(content)
            self.write(chr(26))
        else:
            self.log(f"Ignoring message {content} from {recipient}")

    def disconnect_phone(self):
        self.ser.close()
        self.ser = None

    @staticmethod
    def print_all(messages):
        for message in messages:
            print(message)

    def read(self):
        data = []
        lines = self.ser.readlines()
        for line in lines:
            s = line.decode('utf-8').strip()
            if len(s) > 0:
                data.append(s)
        # self.print_all(data)
        return data

    def get_mems(self):
        a = self.write('AT+CIND=?')
        self.log(a)
        a = self.write('AT+CIND?')
        self.log(a)
        output = self.write('AT+CPMS=?')
        if len(output) == 2 and output[1] == 'OK':
            brackets = re.findall("\((.*?)\)", output[0])
            return brackets[0].replace('"', '').split(',')
        else:
            return None

    def get_all_sms_in_mem(self, mem):
        y = []
        self.log(f"reading sms messages in {mem}")
        self.write('AT+CPMS="' + mem + '"')
        # a = self.write('AT+CMGL="REC UNREAD"', wait=0)
        a = self.write('AT+CMGL="ALL"', wait=0)
        z = []
        for x in a:
            if x.startswith('+CMGL:'):
                r = a.index(x)
                t = r + 1
                z.append(r)
                z.append(t)
            else:
                self.log(f"not a message: {x}")
        for x in z:
            self.log(f"message: {a[x]}")
            y.append(a[x])
        return y

    def read_sms(self):
        self.log("reading sms messages")
        self.write('AT+CMGF=1')
        mems = self.get_mems()
        y = []
        if mems is not None:
            for mem in mems:
                y.extend(self.get_all_sms_in_mem(mem))
        else:
            y.extend(self.get_all_sms_in_mem('SM'))

        self.write('AT+CMGF=0')
        return y

    def delete_read_sms(self):
        self.log("deleting read")
        self.write('AT+CMGF=0')
        mems = self.get_mems()
        y = []
        if mems is not None:
            for mem in mems:
                self.write('AT+CPMS="' + mem + '"')
                self.write('AT+CMGD=0,1')
        else:
            self.write('AT+CMGD=0,1')

        self.write('AT+CMGF=1')

    def reset_modem(self):
        i = 0
        while i < 5:
            replies = self.write('ATZ')
            if self.match_reply(replies, 'OK'):
                return self.ser
            else:
                self.log(f"unable to reset modem, sleeping for {i + 2} ({replies})")
                time.sleep(2 + i)
                i = i + 1
        self.log("unable to reset modem, giving up")
        raise ConnectionError("unable to reset modem, giving up")

    def match_reply(self, replies, message):
        for reply in replies:
            if reply == message:
                return True
        return False