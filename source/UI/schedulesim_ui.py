# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'schedulesim.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from source.UI.mplwidget import MplWidget
import sys


class Ui_MplMainWindow(object):
    def __init__(self):
        self.centralwidget = QtWidgets.QWidget()
        self.SettingsBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mplwidget = MplWidget(self.centralwidget)
        self.Algorithm2String = QtWidgets.QLabel(self.SettingsBox)
        self.SettingsString = QtWidgets.QLabel(self.SettingsBox)
        self.SimulationEnvString = QtWidgets.QLabel(self.SettingsBox)
        self.AlgorithmTypeString = QtWidgets.QLabel(self.SettingsBox)
        self.AlgorithmString = QtWidgets.QLabel(self.SettingsBox)
        self.AlgorithmSelector = QtWidgets.QComboBox(self.SettingsBox)
        self.SimulationConfigString = QtWidgets.QLabel(self.SettingsBox)
        self.NoteString = QtWidgets.QLabel(self.SettingsBox)
        self.RunsGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.RunsGroup)
        self.RunsString = QtWidgets.QLabel(self.RunsGroup)
        self.RunsSpinBox = QtWidgets.QSpinBox(self.RunsGroup)
        self.ProcessesGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.ProcessesGroup)
        self.ProcessesString = QtWidgets.QLabel(self.ProcessesGroup)
        self.ProcessesSpinBox = QtWidgets.QSpinBox(self.ProcessesGroup)
        self.ProcessPropString = QtWidgets.QLabel(self.SettingsBox)
        self.ArrivalGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.ArrivalGroup)
        self.ArrivalTimesString = QtWidgets.QLabel(self.ArrivalGroup)
        self.ArrivalTimesValueBox = QtWidgets.QPlainTextEdit(self.ArrivalGroup)
        self.BurstGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.BurstGroup)
        self.BurstTimesString = QtWidgets.QLabel(self.BurstGroup)
        self.BurstTimesValueBox = QtWidgets.QPlainTextEdit(self.BurstGroup)
        self.TimeQuantumGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.TimeQuantumGroup)
        self.TimeQuantumString = QtWidgets.QLabel(self.TimeQuantumGroup)
        self.TimeQuantumSpinBox = QtWidgets.QSpinBox(self.TimeQuantumGroup)
        self.LoadPropertiesButton = QtWidgets.QPushButton(self.SettingsBox)
        self.SaveResultsButton = QtWidgets.QPushButton(self.SettingsBox)
        self.StartSimulationButton = QtWidgets.QPushButton(self.SettingsBox)
        self.Algorithm2Selector = QtWidgets.QComboBox(self.SettingsBox)
        self.StaticDynamicGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.StaticDynamicGroup)
        self.StaticAlgorithmRadio = QtWidgets.QRadioButton(self.StaticDynamicGroup)
        self.DynamicAlgorithmRadio = QtWidgets.QRadioButton(self.StaticDynamicGroup)
        self.MultithreadMultiprocGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.MultithreadMultiprocGroup)
        self.MultithreadingRadio = QtWidgets.QRadioButton(self.MultithreadMultiprocGroup)
        self.MultiprocessingRadio = QtWidgets.QRadioButton(self.MultithreadMultiprocGroup)
        self.CustomRandomGroup = QtWidgets.QGroupBox(self.SettingsBox)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.CustomRandomGroup)
        self.CustomDataRadio = QtWidgets.QRadioButton(self.CustomRandomGroup)
        self.RandomizedDataRadio = QtWidgets.QRadioButton(self.CustomRandomGroup)

    def setupUi(self, MplMainWindow):
        MplMainWindow.setObjectName("MplMainWindow")
        MplMainWindow.resize(1920, 1080)
        MplMainWindow.setWindowTitle("Schedule Simulator")
        self.centralwidget.setObjectName("centralwidget")
        self.mplwidget.setGeometry(QtCore.QRect(11, 11, 1611, 1058))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplwidget.sizePolicy().hasHeightForWidth())
        self.mplwidget.setSizePolicy(sizePolicy)
        self.mplwidget.setObjectName("mplwidget")
        self.SettingsBox.setGeometry(QtCore.QRect(1637, 11, 271, 1058))
        self.SettingsBox.setTitle("")
        self.SettingsBox.setObjectName("SettingsBox")
        self.SettingsString.setGeometry(QtCore.QRect(10, 0, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.SettingsString.setFont(font)
        self.SettingsString.setObjectName("SettingsString")
        self.SimulationEnvString.setGeometry(QtCore.QRect(10, 70, 190, 16))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.SimulationEnvString.setFont(font)
        self.SimulationEnvString.setObjectName("SimulationEnvString")
        self.AlgorithmTypeString.setGeometry(QtCore.QRect(10, 140, 190, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.AlgorithmTypeString.setFont(font)
        self.AlgorithmTypeString.setObjectName("AlgorithmTypeString")
        self.AlgorithmString.setGeometry(QtCore.QRect(10, 230, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.AlgorithmString.setFont(font)
        self.AlgorithmString.setObjectName("AlgorithmString")
        self.AlgorithmSelector.setGeometry(QtCore.QRect(10, 260, 251, 22))
        self.AlgorithmSelector.setObjectName("AlgorithmSelector")
        self.SimulationConfigString.setGeometry(QtCore.QRect(10, 350, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.SimulationConfigString.setFont(font)
        self.SimulationConfigString.setObjectName("SimulationConfigString")
        self.NoteString.setGeometry(QtCore.QRect(10, 430, 241, 51))
        self.NoteString.setObjectName("NoteString")
        self.RunsGroup.setGeometry(QtCore.QRect(10, 490, 251, 51))
        self.RunsGroup.setTitle("")
        self.RunsGroup.setObjectName("RunsGroup")
        self.horizontalLayout.setObjectName("horizontalLayout")
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.RunsString.setFont(font)
        self.RunsString.setObjectName("RunsString")
        self.horizontalLayout.addWidget(self.RunsString)
        self.RunsSpinBox.setObjectName("RunsSpinBox")
        self.horizontalLayout.addWidget(self.RunsSpinBox)
        self.ProcessesGroup.setGeometry(QtCore.QRect(10, 540, 251, 51))
        self.ProcessesGroup.setTitle("")
        self.ProcessesGroup.setObjectName("ProcessesGroup")
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.ProcessesString.setFont(font)
        self.ProcessesString.setObjectName("ProcessesString")
        self.horizontalLayout_2.addWidget(self.ProcessesString)
        self.ProcessesSpinBox.setObjectName("ProcessesSpinBox")
        self.horizontalLayout_2.addWidget(self.ProcessesSpinBox)
        self.ProcessPropString.setGeometry(QtCore.QRect(10, 600, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.ProcessPropString.setFont(font)
        self.ProcessPropString.setObjectName("ProcessPropString")
        self.ArrivalGroup.setGeometry(QtCore.QRect(10, 680, 251, 61))
        self.ArrivalGroup.setTitle("")
        self.ArrivalGroup.setObjectName("ArrivalGroup")
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.ArrivalTimesString.setFont(font)
        self.ArrivalTimesString.setObjectName("ArrivalTimesString")
        self.horizontalLayout_3.addWidget(self.ArrivalTimesString)
        self.ArrivalTimesValueBox.setObjectName("ArrivalTimesValueBox")
        self.horizontalLayout_3.addWidget(self.ArrivalTimesValueBox)
        self.BurstGroup.setGeometry(QtCore.QRect(10, 740, 251, 61))
        self.BurstGroup.setTitle("")
        self.BurstGroup.setObjectName("BurstGroup")
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.BurstTimesString.setFont(font)
        self.BurstTimesString.setObjectName("BurstTimesString")
        self.horizontalLayout_4.addWidget(self.BurstTimesString)
        self.BurstTimesValueBox.setObjectName("BurstTimesValueBox")
        self.horizontalLayout_4.addWidget(self.BurstTimesValueBox)
        self.TimeQuantumGroup.setGeometry(QtCore.QRect(10, 630, 251, 51))
        self.TimeQuantumGroup.setTitle("")
        self.TimeQuantumGroup.setObjectName("TimeQuantumGroup")
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.TimeQuantumString.setFont(font)
        self.TimeQuantumString.setObjectName("TimeQuantumString")
        self.horizontalLayout_5.addWidget(self.TimeQuantumString)
        self.TimeQuantumSpinBox.setObjectName("TimeQuantumSpinBox")
        self.horizontalLayout_5.addWidget(self.TimeQuantumSpinBox)
        self.LoadPropertiesButton.setGeometry(QtCore.QRect(10, 810, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.LoadPropertiesButton.setFont(font)
        self.LoadPropertiesButton.setObjectName("LoadPropertiesButton")
        self.SaveResultsButton.setGeometry(QtCore.QRect(10, 840, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.SaveResultsButton.setFont(font)
        self.SaveResultsButton.setObjectName("SaveResultsButton")
        self.StartSimulationButton.setGeometry(QtCore.QRect(10, 880, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StartSimulationButton.setFont(font)
        self.StartSimulationButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                 "color: rgb(255, 255, 255);")
        self.StartSimulationButton.setAutoDefault(False)
        self.StartSimulationButton.setDefault(False)
        self.StartSimulationButton.setFlat(False)
        self.StartSimulationButton.setObjectName("StartSimulationButton")
        self.Algorithm2String.setGeometry(QtCore.QRect(10, 290, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.Algorithm2String.setFont(font)
        self.Algorithm2String.setObjectName("Algorithm2String")
        self.Algorithm2Selector.setGeometry(QtCore.QRect(10, 320, 251, 22))
        self.Algorithm2Selector.setObjectName("Algorithm2Selector")
        self.StaticDynamicGroup.setGeometry(QtCore.QRect(10, 170, 167, 47))
        self.StaticDynamicGroup.setTitle("")
        self.StaticDynamicGroup.setObjectName("StaticDynamicGroup")
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.StaticAlgorithmRadio.setObjectName("StaticAlgorithmRadio")
        self.horizontalLayout_6.addWidget(self.StaticAlgorithmRadio)
        self.DynamicAlgorithmRadio.setObjectName("DynamicAlgorithmRadio")
        self.horizontalLayout_6.addWidget(self.DynamicAlgorithmRadio)
        self.MultithreadMultiprocGroup.setGeometry(QtCore.QRect(10, 90, 251, 47))
        self.MultithreadMultiprocGroup.setTitle("")
        self.MultithreadMultiprocGroup.setFlat(False)
        self.MultithreadMultiprocGroup.setObjectName("MultithreadMultiprocGroup")
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.MultithreadingRadio.setObjectName("MultithreadingRadio")
        self.horizontalLayout_7.addWidget(self.MultithreadingRadio)
        self.MultiprocessingRadio.setObjectName("MultiprocessingRadio")
        self.horizontalLayout_7.addWidget(self.MultiprocessingRadio)
        self.CustomRandomGroup.setGeometry(QtCore.QRect(10, 380, 251, 41))
        self.CustomRandomGroup.setTitle("")
        self.CustomRandomGroup.setObjectName("CustomRandomGroup")
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.CustomDataRadio.setObjectName("CustomDataRadio")
        self.horizontalLayout_8.addWidget(self.CustomDataRadio)
        self.RandomizedDataRadio.setObjectName("RandomizedDataRadio")
        self.horizontalLayout_8.addWidget(self.RandomizedDataRadio)
        MplMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MplMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MplMainWindow)

    def retranslateUi(self, MplMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MplMainWindow.setWindowTitle(_translate("MplMainWindow", "MainWindow"))
        self.SettingsString.setText(_translate("MplMainWindow", "Settings"))
        self.SimulationEnvString.setText(_translate("MplMainWindow", "Simulation Environment"))
        self.AlgorithmTypeString.setText(_translate("MplMainWindow", "Algorithm Type"))
        self.AlgorithmString.setText(_translate("MplMainWindow", "Algorithm 1"))
        self.SimulationConfigString.setText(_translate("MplMainWindow", "Simulation Configuration"))
        self.NoteString.setText(_translate("MplMainWindow", "<html><head/><body><p align=\"center\"><span style=\" "
                                                            "font-weight:600; color:#ff0004;\">Note:</span><span "
                                                            "style=\" color:#ff0004;\"> Custom data input will only "
                                                            "allow <br/>up to 3 simulation runs and up to 5 "
                                                            "<br/>processes for each run.</span></p></body></html>"))
        self.RunsString.setText(_translate("MplMainWindow", "Number of Runs:"))
        self.ProcessesString.setText(_translate("MplMainWindow", "Number of Processes:"))
        self.ProcessPropString.setText(_translate("MplMainWindow", "Process Properties:"))
        self.ArrivalTimesString.setText(_translate("MplMainWindow", "Arrival Times:"))
        self.BurstTimesString.setText(_translate("MplMainWindow", "Burst Times:"))
        self.TimeQuantumString.setText(_translate("MplMainWindow", "Time Quantum:"))
        self.LoadPropertiesButton.setText(_translate("MplMainWindow", "Load Properties"))
        self.SaveResultsButton.setText(_translate("MplMainWindow", "Save Results"))
        self.StartSimulationButton.setText(_translate("MplMainWindow", "Start Simulation"))
        self.Algorithm2String.setText(_translate("MplMainWindow", "Algorithm 2"))
        self.StaticAlgorithmRadio.setText(_translate("MplMainWindow", "NonRealTime"))
        self.DynamicAlgorithmRadio.setText(_translate("MplMainWindow", "RealTime"))
        self.MultithreadingRadio.setText(_translate("MplMainWindow", "Multithreading"))
        self.MultiprocessingRadio.setText(_translate("MplMainWindow", "Multiprocessing"))
        self.CustomDataRadio.setText(_translate("MplMainWindow", "Custom Data"))
        self.RandomizedDataRadio.setText(_translate("MplMainWindow", "Random Data"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MplMainWindow = QtWidgets.QMainWindow()
    ui = Ui_MplMainWindow()
    ui.setupUi(MplMainWindow)
    MplMainWindow.show()
    sys.exit(app.exec_())
