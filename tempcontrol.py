import logging

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


class TemperatureController:
    setpoint = 0
    time_period = 60 # time in seconds to wait between control actions

    control_pin = 0
    enabled = False

    def __init__(self, control_pin, time_period):
        self.control_pin = control_pin
        self.time_period = time_period
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(control_pin, GPIO.OUT, initial=GPIO.LOW)

    def control(self, temp):
        if self.enabled:
            if self.control_pin <= 0:
                try:
                    if temp < self.setpoint:
                        self.heat_on()
                    else:
                        self.heat_off()
                except Exception as e:
                    log.error(e)
            else:
                log.error("Control pin not greater than 0")

    def heat_on(self):
        if self.control_pin >= 0:
            GPIO.output(self.control_pin, GPIO.HIGH)
            log.info('Turning heater ON')
        else:
            log.error("Control pin not greater than 0")

    def heat_off(self):
        if self.control_pin >= 0:
            GPIO.output(self.control_pin, GPIO.LOW)
            log.info('Turning heater OFF')
        else:
            log.error("Control pin not greater than 0")

    def cleanup(self):
        GPIO.cleanup()