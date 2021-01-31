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

        # self.MultithreadingRadio.clicked.connect(self.check)
        # self.MultiprocessingRadio.clicked.connect(self.check)
        self.StaticAlgorithmRadio.clicked.connect(self.update_algo_list)
        self.DynamicAlgorithmRadio.clicked.connect(self.update_algo_list)
        self.RandomizedDataRadio.clicked.connect(self.disable_prop_options)
        self.CustomDataRadio.clicked.connect(self.disable_prop_options)
        # self.StartSimulationButton.clicked(self.start_simulation)
        self.RunsSpinBox.setMaximum(3)
        self.ProcessesSpinBox.setMaximum(5)

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

    def generate_random_data(self):
        if self.AlgorithmSelector.currentText() == 'Round-Robin':
            rr = RoundRobin()
            quantum = random.randint(0, 10)
            processData = []
            waitRR = []
            # for i in range:

    # def start_simulation(self):
    # if self.RandomizedDataRadio.isChecked():


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
