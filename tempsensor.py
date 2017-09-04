import time
import logging
import os.path

DEVICE_PATH = '/sys/bus/w1/devices/28-00000'

log = logging.getLogger('TemperatureSensor')
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)


class TemperatureSensor:
    id = ""
    tempC = 0
    setpointC = 0
    sampling_interval = 1 # in seconds

    def __init__(self, id = "", setpointC = 20, sampling_interval = 1):
        self.id = id
        self.setpointC = setpointC
        self.sampling_interval = sampling_interval

    def update(self):
        self.tempC = self.read_temp()

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def read_temp_raw(self):
        f = open(DEVICE_PATH + self.id + '/w1_slave')
        lines = f.readlines()
        return lines

    def test(self):
        return os.path.isfile(DEVICE_PATH + self.id + '/w1_slave')
