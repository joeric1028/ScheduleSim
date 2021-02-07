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

        self.LoadPropertiesButton.clicked.connect(self.load_data)

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

    def load_data(self):
        data = QtWidgets.QFileDialog(parent=self)
        data.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        data.setViewMode(QtWidgets.QFileDialog.List)
        data.setNameFilter(self.tr("Save File (*.sav)"))
        directory = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DocumentsLocation)
        data.setDirectory(directory[0])
        if data.exec():
            filename = data.selectedFiles()
            File = QtCore.QFile(parent=self, name=filename[0])
            if not File.open(QtCore.QIODevice.ReadOnly):
                logging.warning(f"Error opening File: {filename}")
                return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
