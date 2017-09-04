import sys
import threading
import time
import logging
from tempsensor import TemperatureSensor
import datalogging
import persist

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

SETTINGS_FILE = 'persist.json'


class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    TSRed = TemperatureSensor()
    TSBlue = TemperatureSensor()
    TSGreen = TemperatureSensor()
    debouncer = 0

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.clockTick() # start clock
        self.tRedId.textChanged.connect(self.id_debouncer)
        self.tBlueID.textChanged.connect(self.id_debouncer)
        self.tGreenId.textChanged.connect(self.id_debouncer)
        self.load_persistent_settings()

    def load_persistent_settings(self):
        persist.load(SETTINGS_FILE)

        if 'red_id' in persist.settings:
            self.tRedId.setText(persist.settings['red_id'])

        if 'blue_id' in persist.settings:
            self.tBlueID.setText(persist.settings['blue_id'])

        if 'green_id' in persist.settings:
            self.tGreenId.setText(persist.settings['green_id'])

    def clockTick(self):
        self.tTime.setText('{}'.format(time.strftime("%H:%M:%S")))
        timer = threading.Timer(1, self.clockTick)
        timer.start()

    def start_new_timer(self):
        pass

    def log_data(self):
        datalogging.log_data(self.TSRed.tempC, self.TSBlue.tempC, self.TSGreen.tempC)

    def id_debouncer(self):
        if self.debouncer != 0:
            self.debouncer.cancel()
        self.debouncer = threading.Timer(0.5, self.check_valid_id, [self.sender()])
        self.debouncer.start()

    def check_valid_id(self, sender):
        log.info(sender.objectName())

        if sender.objectName() == 'tRedId':
            label = self.lRedOK
            sensor = self.TSRed
            sensor.id = self.tRedId.text()
            persist.settings['red_id'] = sensor.id
        elif sender.objectName() == 'tBlueID':
            label = self.lBlueOK
            sensor = self.TSBlue
            sensor.id = self.tBlueID.text()
            persist.settings['blue_id'] = sensor.id
        else:
            label = self.lGreenOK
            sensor = self.TSGreen
            sensor.id = self.tGreenId.text()
            persist.settings['green_id'] = sensor.id

        persist.save(SETTINGS_FILE)

        if sensor.test():
            label.setText("OK")
            label.setStyleSheet("color: green")
        else:
            label.setText("NOK")
            label.setStyleSheet("color: red")

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()


def main():
    log.info('Starting app...')
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()