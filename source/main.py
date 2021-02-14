from __future__ import with_statement
import numpy as np
import sys
import random
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from source.Library.UI.schedulesim_ui import Ui_MplMainWindow
from source.Library.Algorithms.NonRealTime.RoundRobin import *
import logging
import json

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %('
                           'message)s')

logger = logging.getLogger(__name__)


class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MplMainWindow):
    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.MultithreadingRadio.clicked.connect(self.data_verification)
        self.MultiprocessingRadio.clicked.connect(self.data_verification)
        self.StaticAlgorithmRadio.clicked.connect(self.update_algo_list)
        self.DynamicAlgorithmRadio.clicked.connect(self.update_algo_list)
        self.RandomizedDataRadio.clicked.connect(self.disable_prop_options)
        self.CustomDataRadio.clicked.connect(self.disable_prop_options)
        self.StartSimulationButton.clicked.connect(self.start_simulation)

        self.MultithreadingRadio.toggled.connect(self.data_verification)
        self.MultiprocessingRadio.toggled.connect(self.data_verification)
        self.StaticAlgorithmRadio.toggled.connect(self.update_algo_list)
        self.DynamicAlgorithmRadio.toggled.connect(self.update_algo_list)
        self.RandomizedDataRadio.toggled.connect(self.disable_prop_options)
        self.CustomDataRadio.toggled.connect(self.disable_prop_options)

        self.LoadPropertiesButton.clicked.connect(self.load_prop_data)
        # TODO: Temporary used Save Results Button to Save Properties
        self.SaveResultsButton.clicked.connect(self.save_prop_data)

        self.setWindowTitle("Schedule Simulator v0.01")
        self.RunsSpinBox.setMaximum(3)
        self.ProcessesSpinBox.setMaximum(5)
        self.data_verification()

        self.data = []

    def update_algo_list(self):

        if self.StaticAlgorithmRadio.isChecked():
            self.AlgorithmSelector.clear()
            self.Algorithm2Selector.clear()
            self.AlgorithmSelector.addItems(['Round-Robin', 'Shortest Job First'])
            self.Algorithm2Selector.addItems(['Round-Robin', 'Shortest Job First'])
        elif self.DynamicAlgorithmRadio.isChecked():
            self.AlgorithmSelector.clear()
            self.Algorithm2Selector.clear()
            self.AlgorithmSelector.addItems(['Rate Monotonic Scheduling', 'Earliest Deadline First'])
            self.Algorithm2Selector.addItems(['Rate Monotonic Scheduling', 'Earliest Deadline First'])

        self.data_verification()

    def disable_prop_options(self):
        if self.RandomizedDataRadio.isChecked():
            self.RunsGroup.setEnabled(False)
            self.ProcessesGroup.setEnabled(False)
            self.TimeQuantumGroup.setEnabled(False)
            self.ArrivalGroup.setEnabled(False)
            self.BurstGroup.setEnabled(False)
        elif self.CustomDataRadio.isChecked():
            self.RunsGroup.setEnabled(True)
            self.ProcessesGroup.setEnabled(True)
            self.TimeQuantumGroup.setEnabled(True)
            self.ArrivalGroup.setEnabled(True)
            self.BurstGroup.setEnabled(True)

        self.data_verification()

    def generate_random_data(self):
        if self.RandomizedDataRadio.isChecked():
            testrun = random.randint(1, 3)
            if self.StaticAlgorithmRadio.isChecked():
                if self.AlgorithmSelector.currentIndex(0):  # Round Robin
                    quantum = random.randint(0, 10)
                    processdata = []
                    for i in range(testrun):
                        temp_rr = []
                        process_id = i + 1
                        arrival_time = random.randint(0, 100000)
                        burst_time = random.randint(0, 75000)
                        temp_rr.extend([process_id, arrival_time, burst_time, 0, burst_time])
                        processdata.append(temp_rr)
                elif self.AlgorithmSelector.currentIndex(1):  # Shortest Job First
                    processdata = []
                    for i in range(testrun):
                        temp_sjf = []
                        process_id = i + 1
                        arrival_time = random.randint(0, 100000)
                        burst_time = random.randint(0, 75000)
                        temp_sjf.extend([process_id, arrival_time, burst_time, 0])
                        processdata.append(temp_sjf)
            elif self.DynamicAlgorithmRadio.isChecked():
                if self.Algorithm2Selector.currentIndex(0):  # Rate Monotonic Scheduling
                    rr = RoundRobin()
                    quantum = random.randint(0, 10)
                    processData = []
                    waitRR = []
                    # for i in range:
                elif self.Algorithm2Selector.currentIndex(1):  # Earliest Deadline First
                    pass

    def start_simulation(self):
        pass

    def data_verification(self):
        if (self.MultithreadingRadio.isChecked() or self.MultiprocessingRadio.isChecked()) and \
                (self.StaticAlgorithmRadio.isChecked() or self.DynamicAlgorithmRadio.isChecked()) and \
                (self.AlgorithmSelector.currentIndex() != -1 or self.Algorithm2Selector.currentIndex() != -1) and \
                (self.CustomDataRadio.isChecked() or self.RandomizedDataRadio.isChecked()):
            self.StartSimulationButton.setEnabled(True)
            self.StartSimulationButton.setStyleSheet("background-color: rgb(255, 0, 0);color: rgb(255, 255, 255);")
        else:
            self.StartSimulationButton.setDisabled(True)
            self.StartSimulationButton.setStyleSheet("")

    def load_prop_data(self):
        data = QtWidgets.QFileDialog(parent=self)
        data.setWindowTitle("Open Properties Save File")
        data.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        data.setViewMode(QtWidgets.QFileDialog.List)
        data.setNameFilter(self.tr("Properties Save File (*.sav)"))
        directory = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DocumentsLocation)
        data.setDirectory(directory[0])
        if data.exec():
            filename = data.selectedFiles()
            datafile = open(filename[0], "r")
            if not datafile.errors:
                datafile.close()
                logging.warning(f"Error opening File: {filename}")
                message = QtWidgets.QMessageBox(parent=self)
                message.setText(f"Error opening File: {filename}")
                message.setWindowTitle(self.windowTitle())
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec()
                return

            jsondata = json.loads(datafile.read())
            datafile.close()

            if int(jsondata["simulationmode"]) == 0:
                self.MultithreadingRadio.setChecked(True)
            else:
                self.MultiprocessingRadio.setChecked(True)

            if int(jsondata["algorithmtype"]) == 0:
                self.StaticAlgorithmRadio.setChecked(True)
            else:
                self.DynamicAlgorithmRadio.setChecked(True)

            self.AlgorithmSelector.setCurrentIndex(int(jsondata["algorithm1"]))
            self.Algorithm2Selector.setCurrentIndex(int(jsondata["algorithm2"]))

            if int(jsondata["simulationconfig"]) == 0:
                self.CustomDataRadio.setChecked(True)
                if jsondata["data"] is not None:
                    self.RunsSpinBox.setValue(int(jsondata["data"]["runs"]))
                    self.ProcessesSpinBox.setValue(int(jsondata["data"]["processes"]))
                    self.TimeQuantumSpinBox.setValue(int(jsondata["data"]["timequantum"]))
                    self.ArrivalTimesValueBox.setPlainText(str(jsondata["data"]["arrivaltimes"]))
                    self.BurstTimesValueBox.setPlainText(str(jsondata["data"]["burstimes"]))
                else:
                    self.RunsSpinBox.setValue(0)
                    self.ProcessesSpinBox.setValue(0)
                    self.TimeQuantumSpinBox.setValue(0)
                    self.ArrivalTimesValueBox.clear()
                    self.BurstTimesValueBox.clear()
            else:
                self.RandomizedDataRadio.setChecked(True)

    def save_prop_data(self):
        filename = QtWidgets.QFileDialog(parent=self)
        filename.setWindowTitle("Save Properties Save File")
        filename.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        filename.setViewMode(QtWidgets.QFileDialog.List)
        filename.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        filename.setNameFilters([self.tr("Properties Save File (*.sav)"),
                                 self.tr("Any Files (*)")])
        directory = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DocumentsLocation)
        filename.setDirectory(directory[0])

        if filename.exec():
            datafilename = filename.selectedFiles()[0]
            try:
                createfile = open(datafilename, 'x')
                createfile.close()
            except IOError:
                print(IOError)
            try:
                with open(datafilename, 'w') as json_file:
                    if self.MultithreadingRadio.isChecked() and not self.MultiprocessingRadio.isChecked():
                        simulationmode = 0
                    else:
                        simulationmode = 1

                    if self.StaticAlgorithmRadio.isChecked() and not self.DynamicAlgorithmRadio.isChecked():
                        algorithmtype = 0
                    else:
                        algorithmtype = 1

                    if self.CustomDataRadio.isChecked() and not self.RandomizedDataRadio.isChecked():
                        if self.ArrivalTimesValueBox.toPlainText() is None:
                            arrivaltimes = None
                        else:
                            arrivaltimes = self.ArrivalTimesValueBox.toPlainText()

                        if self.BurstTimesValueBox.toPlainText() is None:
                            burstimes = None
                        else:
                            burstimes = self.BurstTimesValueBox.toPlainText()

                        temp = {
                            "simulationmode": simulationmode,
                            "algorithmtype": algorithmtype,
                            "algorithm1": self.AlgorithmSelector.currentIndex(),
                            "algorithm2": self.Algorithm2Selector.currentIndex(),
                            "simulationconfig": 0,
                            "datafilename":
                                {
                                    "runs": self.RunsSpinBox.value(),
                                    "processes": self.ProcessesSpinBox.value(),
                                    "timequantum": self.TimeQuantumSpinBox.value(),
                                    "arrivaltimes": arrivaltimes,
                                    "burstimes": burstimes
                                }
                        }
                    else:
                        temp = {
                            "simulationmode": simulationmode,
                            "algorithmtype": algorithmtype,
                            "algorithm1": self.AlgorithmSelector.currentIndex(),
                            "algorithm2": self.Algorithm2Selector.currentIndex(),
                            "simulationconfig": 1,
                            "datafilename": None
                        }
                    json.dump(temp, json_file, indent=4)
                print(datafilename)
            except IOError:
                print(IOError)
                logging.warning(f"File '{datafilename}' is currently in use")
                print(f"File '{datafilename}' is currently in use")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
