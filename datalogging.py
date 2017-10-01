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
LOG_INTERVAL = 60

def log_data(*argv):
    global log_counter
    if log_counter >= LOG_INTERVAL:
        log_counter = 0
        message = ','.join(map(str, argv))
        if len(message) > 0:
            brewlogger.info(message)
    else:
        log_counter += 1
