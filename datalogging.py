# This module takes care of logging brew session data

# We will focus on logging to a file first, then implement offloading to a server
import logging
import time

datalogger = logging.getLogger('datalogger')
datalogger.setLevel(logging.INFO)
dataformatter = logging.Formatter('%(asctime)s,%(message)s')
filehandler = logging.FileHandler(filename='brew-' + time.strftime('%Y-%m-%d') + '.log')
filehandler.setFormatter(dataformatter)
datalogger.addHandler(filehandler)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)

def log_data(*argv):
    message = ','.join(map(str, argv))
    if len(message) > 0:
        log.info(message)