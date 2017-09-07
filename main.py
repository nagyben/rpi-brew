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

import brew_auto

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)

SETTINGS_FILE = 'persist.json'


class BrewWindow(QMainWindow, brew_auto.Ui_MainWindow):
    TSRed = TemperatureSensor()
    TSBlue = TemperatureSensor()
    TSGreen = TemperatureSensor()
    debouncer = 0

    prep_start_time = 0
    mash_start_time = 0
    boil_start_time = 0

    timers_to_update = []

    timer = 0

    logging_enabled = False

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.clockTick() # start clock
        self.tRedId.textChanged.connect(self.id_debouncer)
        self.tBlueID.textChanged.connect(self.id_debouncer)
        self.tGreenId.textChanged.connect(self.id_debouncer)
        self.load_persistent_settings()

        self.btnPrep.clicked.connect(self.start_prep)
        self.btnMash.clicked.connect(self.start_mash)
        self.btnBoil.clicked.connect(self.start_boil)

        self.btnLogging.clicked.connect(self.toggle_logging)

        temp_sensors = [
            {'sensor' : TemperatureSensor(),
             'ui_label' : self.lRed,
             'id_textbox' : self.tRedId},
            {'sensor': TemperatureSensor(),
             'ui_label': self.lBlue,
             'id_textbox': self.tBlueId},
            {'sensor': TemperatureSensor(),
             'ui_label': self.lGreen,
             'id_textbox': self.tGreenId}
        ]

    def load_persistent_settings(self):
        persist.load(SETTINGS_FILE)

        if 'red_id' in persist.settings:
            self.tRedId.setText(persist.settings['red_id'])

        if 'blue_id' in persist.settings:
            self.tBlueID.setText(persist.settings['blue_id'])

        if 'green_id' in persist.settings:
            self.tGreenId.setText(persist.settings['green_id'])

    # 1 second timer - update clocks, read temperatures & log data
    def clockTick(self):

        # Update the prep / mash / boil timers
        for timer in self.timers_to_update:
            # timer[0] is the label reference
            # timer[1] is the struct_time when the button was pressed
            hours, remainder = divmod(time.time() - time.mktime(timer[1]), 60 * 60)
            minutes, seconds = divmod(remainder, 60)

            # don't forget the leading spaces for the offset
            #                 vvv
            timer[0].setText(" + {:02d}:{:02d}".format(int(minutes), int(seconds)))

        # Update clock
        self.lTime.setText('{}'.format(time.strftime("%d %b %Y --- %H:%M:%S")))

        # Update temperatures
        self.update_temp()

        # Log data to file
        if self.logging_enabled:
            self.log_data()

        # Next tick
        self.timer = threading.Timer(1, self.clockTick)
        self.timer.start()

    def update_temp(self):
        for

    def toggle_logging(self):
        self.logging_enabled = not self.logging_enabled
        if self.logging_enabled:
            self.btnLogging.setText("LOGGING ENABLED")
            self.btnLogging.setStyleSheet("color: green")
        else:
            self.btnLogging.setText("LOGGING DISABLED")
            self.btnLogging.setStyleSheet("color: red")

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

    def closeEvent(self, event):
        self.timer.cancel()
        event.accept()

    def start_prep(self):
        self.prep_start_time = time.localtime()
        self.lPrepStart.setText(time.strftime('%H:%M', self.prep_start_time))

        # Don't forget the leading spaces for the offset
        #                          vvv
        self.lPrepElapsed.setText(" + 00:00")

        # Add label and related start time to the timer list (fn clock_tick() updates the label)
        self.timers_to_update.append([self.lPrepElapsed, self.prep_start_time])

    def start_mash(self):
        self.mash_start_time = time.localtime()
        self.lMashStart.setText(time.strftime('%H:%M', self.mash_start_time))

        # Don't forget the leading spaces for the offset
        #                          vvv
        self.lMashElapsed.setText(" + 00:00")

        # Add label and related start time to the timer list (fn clock_tick() updates the label)
        self.timers_to_update.append([self.lMashElapsed, self.mash_start_time])

    def start_boil(self):
        self.boil_start_time = time.localtime()
        self.lBoilStart.setText(time.strftime('%H:%M', self.boil_start_time))

        # Don't forget the leading spaces for the offset
        #                          vvv
        self.lBoilElapsed.setText(" + 00:00")

        # Add label and related start time to the timer list (fn clock_tick() updates the label)
        self.timers_to_update.append([self.lBoilElapsed, self.boil_start_time])


def main():
    log.info('Starting app...')
    app = QApplication(sys.argv)
    form = BrewWindow()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()