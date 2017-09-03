import sys
import threading
import time
import logging

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import mainwindow_auto

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)


class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.clockTick()
        log.info("herp")
        self.setMouseTracking(True)

    def clockTick(self):
        self.tTime.setText('{}'.format(time.strftime("%H:%M:%S")))
        timer = threading.Timer(1, self.clockTick)
        timer.start()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, QMouseEvent):
        self.statusBar.showMessage('{}, {}'.format(QMouseEvent.x(), QMouseEvent.y()))

def main():
    log.info('Starting app...')
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()