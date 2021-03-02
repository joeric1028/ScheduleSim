import sys
import random
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from source.Library.UI.schedulesim_ui import Ui_MplMainWindow
import json
from source.Library.Common.LoadBalancer import LoadBalancer


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
        self.AlgorithmSelector.currentIndexChanged.connect(self.data_verification)
        self.Algorithm2Selector.currentIndexChanged.connect(self.data_verification)
        self.RunsSpinBox.valueChanged.connect(self.data_verification)
        self.ProcessesSpinBox.valueChanged.connect(self.data_verification)
        self.TimeQuantumSpinBox.valueChanged.connect(self.data_verification)
        self.ArrivalTimesValueBox.textChanged.connect(self.data_verification)
        self.BurstTimesValueBox.textChanged.connect(self.data_verification)

        self.MultithreadingRadio.toggled.connect(self.data_verification)
        self.MultiprocessingRadio.toggled.connect(self.data_verification)
        self.StaticAlgorithmRadio.toggled.connect(self.update_algo_list)
        self.DynamicAlgorithmRadio.toggled.connect(self.update_algo_list)
        self.RandomizedDataRadio.toggled.connect(self.disable_prop_options)
        self.CustomDataRadio.toggled.connect(self.disable_prop_options)

        self.LoadPropertiesButton.clicked.connect(self.load_prop_data)
        self.SavePropertiesButton.clicked.connect(self.save_prop_data)

        self.setWindowTitle("Schedule Simulator v0.0.1")
        self.RunsSpinBox.setMaximum(3)
        self.ProcessesSpinBox.setMaximum(5)
        self.TimeQuantumSpinBox.setMaximum(10)
        self.data_verification()

        # TODO: Test Display of Graph
        self.mplwidget.canvas.ax.set_title("Round Robin vs Shortest Job First Testing")
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times")
        self.mplwidget.canvas.ax.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40], label="text")
        self.mplwidget.canvas.ax.legend()

        self.processdata = []
        self.result = []

    def update_algo_list(self):
        if self.StaticAlgorithmRadio.isChecked():
            self.AlgorithmSelector.clear()
            self.Algorithm2Selector.clear()
            self.AlgorithmSelector.addItems(['Round Robin', 'Shortest Job First'])
            self.Algorithm2Selector.addItems(['Round Robin', 'Shortest Job First'])
        elif self.DynamicAlgorithmRadio.isChecked():
            self.AlgorithmSelector.clear()
            self.Algorithm2Selector.clear()
            self.AlgorithmSelector.addItems(['Rate Monotonic Scheduling', 'Earliest Deadline First'])
            self.Algorithm2Selector.addItems(['Rate Monotonic Scheduling', 'Earliest Deadline First'])

        self.AlgorithmSelector.setCurrentIndex(0)
        self.Algorithm2Selector.setCurrentIndex(1)

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
            testrun = random.randint(1, self.RunsSpinBox.maximum())
            testprocesses = random.randint(2, self.ProcessesSpinBox.maximum())
            self.RunsSpinBox.setValue(testrun)
            self.ProcessesSpinBox.setValue(testprocesses)
            self.ArrivalTimesValueBox.clear()
            self.BurstTimesValueBox.clear()
            tempprocessdata = []

            if self.StaticAlgorithmRadio.isChecked():
                quantum = random.randint(1, self.TimeQuantumSpinBox.maximum())
                self.TimeQuantumSpinBox.setValue(quantum)

                for i in range(testrun):
                    temprunsdataRR = []
                    temprunsdataSJF = []

                    for j in range(testprocesses):
                        temp_dataRR = []
                        temp_dataSJF = []
                        process_id = j + 1
                        arrival_time = random.randint(0, 100000)
                        burst_time = random.randint(0, 75000)
                        temp_dataRR.extend([process_id, arrival_time, burst_time, 0, burst_time])
                        temp_dataSJF.extend([process_id, arrival_time, burst_time, 0])
                        if self.ArrivalTimesValueBox.toPlainText() != "":
                            self.ArrivalTimesValueBox.setPlainText(self.ArrivalTimesValueBox.toPlainText() + ","
                                                                   + str(arrival_time))
                        else:
                            self.ArrivalTimesValueBox.setPlainText(str(arrival_time))

                        if self.BurstTimesValueBox.toPlainText() != "":
                            self.BurstTimesValueBox.setPlainText(self.BurstTimesValueBox.toPlainText() + ","
                                                                 + str(burst_time))
                        else:
                            self.BurstTimesValueBox.setPlainText(str(burst_time))
                        temprunsdataRR.append(temp_dataRR)
                        temprunsdataSJF.append(temp_dataSJF)
                    tempprocessdata.append([0, temprunsdataRR, quantum])
                    tempprocessdata.append([1, temprunsdataSJF, 0])
            elif self.DynamicAlgorithmRadio.isChecked():
                if self.Algorithm2Selector.currentIndex(0):  # Rate Monotonic Scheduling
                    pass
                elif self.Algorithm2Selector.currentIndex(1):  # Earliest Deadline First
                    pass
            self.processdata = tempprocessdata

    def start_simulation(self):
        # TODO: Test Display of Graph using Start Simulation tool
        self.mplwidget.canvas.ax.cla()
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times")
        self.mplwidget.canvas.ax.plot([0, 1, 2, 3, 4], [random.randint(1, 10),
                                                        random.randint(1, 10), random.randint(1, 10),
                                                        random.randint(1, 10), random.randint(1, 10)],
                                      label="plot" + random.randint(1, 10).__str__())
        self.mplwidget.canvas.ax.legend()
        self.mplwidget.canvas.draw()

        self.generate_random_data()

        resultRR = []
        resultSJF = []

        # if self.MultiprocessingRadio.isChecked():
        #     with futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        #         results = executor.map(ThreadWorker, self.processdata)
        #
        #         for f in results:
        #             if f.waitingRR != 0:
        #                 self.result.append([0, f.waitingRR])
        #                 resultRR.append(f.waitingRR)
        #             if f.waitingSJF != 0:
        #                 self.result.append([1, f.waitingSJF])
        #                 resultSJF.append(f.waitingSJF)
        # elif self.MultithreadingRadio.isChecked():
        #     with futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        #         results = executor.map(ThreadWorker, self.processdata)
        #
        #         for f in results:
        #             if f.waitingRR != 0:
        #                 self.result.append([0, f.waitingRR])
        #                 resultRR.append(f.waitingRR)
        #             if f.waitingSJF != 0:
        #                 self.result.append([1, f.waitingSJF])
        #                 resultSJF.append(f.waitingSJF)
        # else:
        #     return

        args_array = {
            # Set some initial CPU load values as a CPU usage goal
            "cpu_target": 0.60,
            # When CPU load is significantly low, start this number
            # of threads
            "thread_group_size": 3
        }

        load1 = LoadBalancer(args_array)

        load1.start_thread_process(self.processdata)
        for f in range(len(load1.results)):
            if load1.results[f][0] != 0:
                self.result.append(load1.results[f])
                resultRR.append(load1.results[f])
            if load1.results[f][0] != 1:
                self.result.append(load1.results[f])
                resultSJF.append(load1.results[f])

        self.mplwidget.canvas.ax.cla()
        self.mplwidget.canvas.ax.set_title("Round Robin vs Shortest Job First Simulation Test")
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times")

        runs = []
        for j in range(len(resultRR)):
            runs.append(j + 1)

        self.mplwidget.canvas.ax.plot(runs, resultRR, label="Round Robin")
        self.mplwidget.canvas.ax.legend()
        self.mplwidget.canvas.draw()
        self.mplwidget.canvas.ax.plot(runs, resultSJF, label="Shortest Job First")
        self.mplwidget.canvas.ax.legend()
        self.mplwidget.canvas.draw()

    def data_verification(self):
        if (self.MultithreadingRadio.isChecked() or self.MultiprocessingRadio.isChecked()) and \
                (self.StaticAlgorithmRadio.isChecked() or self.DynamicAlgorithmRadio.isChecked()) and \
                (self.AlgorithmSelector.currentIndex() != -1 or self.Algorithm2Selector.currentIndex() != -1) and \
                (self.CustomDataRadio.isChecked() or self.RandomizedDataRadio.isChecked()) and \
                (self.AlgorithmSelector.currentIndex() != self.Algorithm2Selector.currentIndex() and
                 self.RandomizedDataRadio.isChecked() or
                 self.CustomDataRadio.isChecked() and
                 (self.RunsSpinBox.value() > 1 and self.ProcessesSpinBox.value() > 1 and
                 self.TimeQuantumSpinBox.value() > 1) and
                 (self.ArrivalTimesValueBox.toPlainText() != "" and self.BurstTimesValueBox.toPlainText() != "")):
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
                print("File is already created!")

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
                        temp = {
                            "simulationmode": simulationmode,
                            "algorithmtype": algorithmtype,
                            "algorithm1": self.AlgorithmSelector.currentIndex(),
                            "algorithm2": self.Algorithm2Selector.currentIndex(),
                            "simulationconfig": 0,
                            "data":
                                {
                                    "runs": self.RunsSpinBox.value(),
                                    "processes": self.ProcessesSpinBox.value(),
                                    "timequantum": self.TimeQuantumSpinBox.value(),
                                    "arrivaltimes": self.ArrivalTimesValueBox.toPlainText(),
                                    "burstimes": self.BurstTimesValueBox.toPlainText()
                                }
                        }
                    else:
                        temp = {
                            "simulationmode": simulationmode,
                            "algorithmtype": algorithmtype,
                            "algorithm1": self.AlgorithmSelector.currentIndex(),
                            "algorithm2": self.Algorithm2Selector.currentIndex(),
                            "simulationconfig": 1,
                            "data": None
                        }
                    json.dump(temp, json_file, indent=4)
                print(datafilename)
            except IOError:
                print(IOError)
                print(f"File '{datafilename}' is currently in use or not accessible")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
