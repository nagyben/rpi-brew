# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../rpi-brew-gui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(648, 391)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 120, 651, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tBlue = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.tBlue.setFont(font)
        self.tBlue.setAlignment(QtCore.Qt.AlignCenter)
        self.tBlue.setObjectName("tBlue")
        self.gridLayout.addWidget(self.tBlue, 0, 1, 1, 1)
        self.tRed = QtWidgets.QLabel(self.gridLayoutWidget)
        self.tRed.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.tRed.setFont(font)
        self.tRed.setAlignment(QtCore.Qt.AlignCenter)
        self.tRed.setObjectName("tRed")
        self.gridLayout.addWidget(self.tRed, 0, 0, 1, 1)
        self.tGreen = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.tGreen.setFont(font)
        self.tGreen.setAlignment(QtCore.Qt.AlignCenter)
        self.tGreen.setObjectName("tGreen")
        self.gridLayout.addWidget(self.tGreen, 0, 2, 1, 1)
        self.tTime = QtWidgets.QLabel(self.centralWidget)
        self.tTime.setGeometry(QtCore.QRect(6, 9, 641, 51))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.tTime.setFont(font)
        self.tTime.setAlignment(QtCore.Qt.AlignCenter)
        self.tTime.setObjectName("tTime")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tBlue.setText(_translate("MainWindow", "###.#"))
        self.tRed.setText(_translate("MainWindow", "###.#"))
        self.tGreen.setText(_translate("MainWindow", "###.#"))
        self.tTime.setText(_translate("MainWindow", "00:00"))

