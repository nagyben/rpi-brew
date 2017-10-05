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
    name = ""
    sensor_id = ""
    tempC = -1

    def __init__(self, name, sensor_id=""):
        if name == "":
            log.error("TemperatureSensor name not defined")
            raise RuntimeError

        self.name = name
        self.sensor_id = sensor_id

    def update(self):
        self.tempC = self.read_temp()
        self.tempC = None if self.tempC == -1 else self.tempC

    def read_temp(self):
        if self.sensor_id == "":
            log.warning("No ID set for sensor {}".format(self.sensor_id))
        else:
            path = DEVICE_PATH + self.sensor_id + '/w1_slave'
            try:
                with open(path) as f:
                    lines = f.readlines()

                    if lines[0].strip()[-3:] == 'YES':
                        return float(lines[1].split('=')[1]) / 1000

                    else:
                        return -1

            except Exception as e:
                log.error(e)
                return -1

    def test(self):
        return os.path.isfile(DEVICE_PATH + self.sensor_id + '/w1_slave')

    def get_string(self):
        if self.tempC > 0:
            return '{} °C'.format(self.tempC)
        else:
            return "n/a"
