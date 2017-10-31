# This module takes care of logging brew session data

# We will focus on logging to a file first, then implement offloading to a server
import logging
import time

brewlogger = logging.getLogger('brewlogger')
brewlogger.setLevel(logging.INFO)
dataformatter = logging.Formatter('%(asctime)s,%(message)s', "%Y-%m-%d %H:%M:%S")
filehandler = logging.FileHandler(filename='brew.log')
filehandler.setFormatter(dataformatter)
brewlogger.addHandler(filehandler)

fermentlogger = logging.getLogger('fermentlogger')
fermentlogger.setLevel(logging.INFO)
dataformatter = logging.Formatter('%(asctime)s,%(message)s', "%Y-%m-%d %H:%M:%S")
filehandler = logging.FileHandler(filename='ferment.log')
filehandler.setFormatter(dataformatter)
fermentlogger.addHandler(filehandler)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)

log_counter = 0
LOG_INTERVAL = 10

last_log_time = 0

def log_brew_data(*argv):
    global last_log_time
    if time.time() - last_log_time >= LOG_INTERVAL:
        last_log_time = time.time()
        message = ','.join(map(str, argv))
        if len(message) > 0:
            brewlogger.info(message)

def log_ferment_data(*argv):
    global last_log_time
    if time.time() - last_log_time >= LOG_INTERVAL:
        last_log_time = time.time()
        message = ','.join(map(str, argv))
        if len(message) > 0:
            fermentlogger.info(message)
