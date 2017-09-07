# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../rpi-brew-gui/brew.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 560)
        MainWindow.setStyleSheet("")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(2, 10, 831, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lTime = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lTime.sizePolicy().hasHeightForWidth())
        self.lTime.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lTime.setFont(font)
        self.lTime.setStyleSheet("color: rgb(85, 87, 83);")
        self.lTime.setAlignment(QtCore.Qt.AlignCenter)
        self.lTime.setObjectName("lTime")
        self.verticalLayout.addWidget(self.lTime)
        self.lMode = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lMode.sizePolicy().hasHeightForWidth())
        self.lMode.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.lMode.setFont(font)
        self.lMode.setAlignment(QtCore.Qt.AlignCenter)
        self.lMode.setObjectName("lMode")
        self.verticalLayout.addWidget(self.lMode)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.lPhase = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lPhase.sizePolicy().hasHeightForWidth())
        self.lPhase.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.lPhase.setFont(font)
        self.lPhase.setAlignment(QtCore.Qt.AlignCenter)
        self.lPhase.setObjectName("lPhase")
        self.verticalLayout.addWidget(self.lPhase)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("padding-left: 50%;\n"
"color:rgb(186, 189, 182);")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 1, 1, 1)
        self.tGreenId = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tGreenId.setStyleSheet("color: green;")
        self.tGreenId.setMaxLength(6)
        self.tGreenId.setAlignment(QtCore.Qt.AlignCenter)
        self.tGreenId.setObjectName("tGreenId")
        self.gridLayout.addWidget(self.tGreenId, 0, 2, 1, 1)
        self.lMashElapsed = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lMashElapsed.sizePolicy().hasHeightForWidth())
        self.lMashElapsed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.lMashElapsed.setFont(font)
        self.lMashElapsed.setStyleSheet("padding-left: 50%")
        self.lMashElapsed.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lMashElapsed.setObjectName("lMashElapsed")
        self.gridLayout.addWidget(self.lMashElapsed, 7, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("padding-left: 50%;\n"
"color:rgb(186, 189, 182);")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 2, 1, 1)
        self.lMashStart = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lMashStart.sizePolicy().hasHeightForWidth())
        self.lMashStart.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        self.lMashStart.setFont(font)
        self.lMashStart.setStyleSheet("padding-left: 50%;\n"
"color:rgb(136, 138, 133)")
        self.lMashStart.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lMashStart.setObjectName("lMashStart")
        self.gridLayout.addWidget(self.lMashStart, 6, 1, 1, 1)
        self.lPrepElapsed = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lPrepElapsed.sizePolicy().hasHeightForWidth())
        self.lPrepElapsed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.lPrepElapsed.setFont(font)
        self.lPrepElapsed.setStyleSheet("padding-left: 50%")
        self.lPrepElapsed.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lPrepElapsed.setObjectName("lPrepElapsed")
        self.gridLayout.addWidget(self.lPrepElapsed, 7, 0, 1, 1)
        self.lRedOK = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lRedOK.sizePolicy().hasHeightForWidth())
        self.lRedOK.setSizePolicy(sizePolicy)
        self.lRedOK.setAlignment(QtCore.Qt.AlignCenter)
        self.lRedOK.setObjectName("lRedOK")
        self.gridLayout.addWidget(self.lRedOK, 2, 0, 1, 1)
        self.lBoilElapsed = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lBoilElapsed.sizePolicy().hasHeightForWidth())
        self.lBoilElapsed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.lBoilElapsed.setFont(font)
        self.lBoilElapsed.setStyleSheet("padding-left: 50%")
        self.lBoilElapsed.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lBoilElapsed.setObjectName("lBoilElapsed")
        self.gridLayout.addWidget(self.lBoilElapsed, 7, 2, 1, 1)
        self.lPrepStart = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lPrepStart.sizePolicy().hasHeightForWidth())
        self.lPrepStart.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        self.lPrepStart.setFont(font)
        self.lPrepStart.setStyleSheet("padding-left: 50%;\n"
"color:rgb(136, 138, 133)")
        self.lPrepStart.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lPrepStart.setObjectName("lPrepStart")
        self.gridLayout.addWidget(self.lPrepStart, 6, 0, 1, 1)
        self.lBlueOK = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lBlueOK.sizePolicy().hasHeightForWidth())
        self.lBlueOK.setSizePolicy(sizePolicy)
        self.lBlueOK.setAlignment(QtCore.Qt.AlignCenter)
        self.lBlueOK.setObjectName("lBlueOK")
        self.gridLayout.addWidget(self.lBlueOK, 2, 1, 1, 1)
        self.btnPrep = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnPrep.setMinimumSize(QtCore.QSize(0, 75))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btnPrep.setFont(font)
        self.btnPrep.setObjectName("btnPrep")
        self.gridLayout.addWidget(self.btnPrep, 4, 0, 1, 1)
        self.tBlueId = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tBlueId.setStyleSheet("color: blue;")
        self.tBlueId.setMaxLength(6)
        self.tBlueId.setAlignment(QtCore.Qt.AlignCenter)
        self.tBlueId.setObjectName("tBlueId")
        self.gridLayout.addWidget(self.tBlueId, 0, 1, 1, 1)
        self.lGreen = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.lGreen.setFont(font)
        self.lGreen.setStyleSheet("color: green;")
        self.lGreen.setAlignment(QtCore.Qt.AlignCenter)
        self.lGreen.setObjectName("lGreen")
        self.gridLayout.addWidget(self.lGreen, 3, 2, 1, 1)
        self.lGreenOK = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lGreenOK.sizePolicy().hasHeightForWidth())
        self.lGreenOK.setSizePolicy(sizePolicy)
        self.lGreenOK.setAlignment(QtCore.Qt.AlignCenter)
        self.lGreenOK.setObjectName("lGreenOK")
        self.gridLayout.addWidget(self.lGreenOK, 2, 2, 1, 1)
        self.lRed = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lRed.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.lRed.setFont(font)
        self.lRed.setAutoFillBackground(False)
        self.lRed.setStyleSheet("color: red;")
        self.lRed.setAlignment(QtCore.Qt.AlignCenter)
        self.lRed.setObjectName("lRed")
        self.gridLayout.addWidget(self.lRed, 3, 0, 1, 1)
        self.btnBoil = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnBoil.setMinimumSize(QtCore.QSize(0, 75))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btnBoil.setFont(font)
        self.btnBoil.setObjectName("btnBoil")
        self.gridLayout.addWidget(self.btnBoil, 4, 2, 1, 1)
        self.btnMash = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnMash.setMinimumSize(QtCore.QSize(0, 75))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btnMash.setFont(font)
        self.btnMash.setObjectName("btnMash")
        self.gridLayout.addWidget(self.btnMash, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("padding-left: 50%;\n"
"color:rgb(186, 189, 182);")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.tRedId = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tRedId.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tRedId.setBaseSize(QtCore.QSize(0, 0))
        self.tRedId.setStyleSheet("color: red;")
        self.tRedId.setMaxLength(6)
        self.tRedId.setAlignment(QtCore.Qt.AlignCenter)
        self.tRedId.setObjectName("tRedId")
        self.gridLayout.addWidget(self.tRedId, 0, 0, 1, 1)
        self.lBlue = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.lBlue.setFont(font)
        self.lBlue.setStyleSheet("color: blue;")
        self.lBlue.setAlignment(QtCore.Qt.AlignCenter)
        self.lBlue.setObjectName("lBlue")
        self.gridLayout.addWidget(self.lBlue, 3, 1, 1, 1)
        self.lBoilStart = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lBoilStart.sizePolicy().hasHeightForWidth())
        self.lBoilStart.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(30)
        self.lBoilStart.setFont(font)
        self.lBoilStart.setStyleSheet("padding-left: 50%;\n"
"color:rgb(136, 138, 133)")
        self.lBoilStart.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lBoilStart.setObjectName("lBoilStart")
        self.gridLayout.addWidget(self.lBoilStart, 6, 2, 1, 1)
        self.btnLogging = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnLogging.setStyleSheet("color: red;")
        self.btnLogging.setObjectName("btnLogging")
        self.gridLayout.addWidget(self.btnLogging, 8, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(4, 6)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RPI Brew v0.1"))
        self.lTime.setText(_translate("MainWindow", "01 January 2017 12:36"))
        self.lMode.setText(_translate("MainWindow", "BREW MODE"))
        self.lPhase.setText(_translate("MainWindow", "PLEASE START PREP"))
        self.label_2.setText(_translate("MainWindow", "hh:mm:ss"))
        self.tGreenId.setPlaceholderText(_translate("MainWindow", "Sensor ID"))
        self.lMashElapsed.setText(_translate("MainWindow", "   ##:##"))
        self.label_3.setText(_translate("MainWindow", "hh:mm:ss"))
        self.lMashStart.setText(_translate("MainWindow", "##:##"))
        self.lPrepElapsed.setText(_translate("MainWindow", "   ##:##"))
        self.lRedOK.setText(_translate("MainWindow", "Enter sensor ID"))
        self.lBoilElapsed.setText(_translate("MainWindow", "   ##:##"))
        self.lPrepStart.setText(_translate("MainWindow", "##:##"))
        self.lBlueOK.setText(_translate("MainWindow", "Enter sensor ID"))
        self.btnPrep.setText(_translate("MainWindow", "Start PREP"))
        self.tBlueId.setPlaceholderText(_translate("MainWindow", "Sensor ID"))
        self.lGreen.setText(_translate("MainWindow", "###.# °C"))
        self.lGreenOK.setText(_translate("MainWindow", "Enter sensor ID"))
        self.lRed.setText(_translate("MainWindow", "###.# °C"))
        self.btnBoil.setText(_translate("MainWindow", "Start BOIL"))
        self.btnMash.setText(_translate("MainWindow", "Start MASH"))
        self.label_4.setText(_translate("MainWindow", "hh:mm:ss"))
        self.tRedId.setPlaceholderText(_translate("MainWindow", "Sensor ID"))
        self.lBlue.setText(_translate("MainWindow", "###.# °C"))
        self.lBoilStart.setText(_translate("MainWindow", "##:##"))
        self.btnLogging.setText(_translate("MainWindow", "LOGGING DISABLED"))

