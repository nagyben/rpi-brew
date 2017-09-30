import logging
import sys

DEVICE_PATH = '/sys/bus/w1/devices/28-00000'

log = logging.getLogger('TemperatureController')
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    log.critical("Error importing RPi.GPIO!  Try using 'sudo'")
    sys.exit(0)
except ImportError:
    log.warning("Module 'RPi.GPIO' not found - using dummy GPIO library")
    import GPIO


class TemperatureController:
    setpoint = 17
    time_period = 60 # time in seconds to wait between control actions

    control_pin = 0
    enabled = False

    heating = 0

    def __init__(self, control_pin, time_period):
        self.control_pin = control_pin
        self.time_period = time_period
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(control_pin, GPIO.OUT, initial=GPIO.LOW)

    def control(self, temp):
        if temp is not None and temp > -1:
            if self.control_pin >= 0:
                try:
                    if temp < self.setpoint and self.heating == 0:
                        self.heat_on()
                    elif temp > self.setpoint and self.heating == 1:
                        self.heat_off()
                except Exception as e:
                    log.error(e)
            else:
                log.error("Control pin not greater than 0")
        else:
            log.error("Temperature not given")
            if self.heating == 1:
                self.heat_off()

    def heat_on(self):
        if self.control_pin >= 0:
            GPIO.output(self.control_pin, GPIO.HIGH)
            self.heating = 1
            log.info('Turning heater ON')
        else:
            log.error("Control pin not greater than 0")

    def heat_off(self):
        if self.control_pin >= 0:
            GPIO.output(self.control_pin, GPIO.LOW)
            self.heating = 0
            log.info('Turning heater OFF')
        else:
            log.error("Control pin not greater than 0")

    def cleanup(self):
        GPIO.cleanup()