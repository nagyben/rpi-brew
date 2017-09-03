import time
import logging

DEVICE_PATH = '/sys/bus/w1/devices/28-00000'

log = logging.getLogger('TemperatureController')
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)


class TemperatureController:
    temp_sensor_id = ""
    setpoint = 0
    time_period = 60 # time in seconds to wait between control actions

    heat_control_pin = 0

    def __init__(self, control_pin, time_period):
        self.control_pin = control_pin
        self.time_period = time_period

    def control(self):
        try:
            if self.read_temp() < self.setpoint:
                self.heat_on()
            else:
                self.heat_off()
        except Exception as e:
            log.error(e)

    def read_temp_raw(self):
        f = open(DEVICE_PATH + self.temp_sensor_id + '/w1_slave')
        lines = f.readlines()
        return lines

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

    def heat_on(self):
        log.info('Turning heater ON')

    def heat_off(self):
        log.info('Turning heater OFF')