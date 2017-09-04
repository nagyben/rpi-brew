import sys
import threading
import time
import logging
from tempsensor import TemperatureSensor
import datalogging

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

import mainwindow_auto

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)


class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    TSRed = TemperatureSensor()
    TSBlue = TemperatureSensor()
    TSGreen = TemperatureSensor()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.clockTick() # start clock
        # redb = QPushButton(self)

    def clockTick(self):
        self.tTime.setText('{}'.format(time.strftime("%H:%M:%S")))
        timer = threading.Timer(1, self.clockTick)
        timer.start()

    def start_new_timer(self):
        pass

    def log_data(self):
        datalogging.log_data(self.TSRed.tempC, self.TSBlue.tempC, self.TSGreen.tempC)

    def herp(self):
        redb = QPushButton(self)



def main():
    log.info('Starting app...')
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    form.gridLayout.addWidget(QPushButton())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()