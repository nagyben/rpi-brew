import logging

log = logging.getLogger('GPIO')
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)

BOARD = "BOARD"
OUT = "OUT"
IN = "IN"
HIGH = 1
LOW = 0

def setmode(mode):
    log.info("Setting pin numbering to {}".format(mode))


def setup(control_pin, direction, initial):
    log.info("Setup of pin {}: {}, initial {}".format(control_pin, direction, initial))


def output(control_pin, output):
    log.info("Setting output of pin {} to {}".format(control_pin, output))


def cleanup():
    log.info("Cleaning up GPIO")