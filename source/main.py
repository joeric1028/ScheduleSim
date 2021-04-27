import json
import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from source.Library.Common.LoadBalancer import LoadBalancer
from source.Library.UI.schedulesim_ui import Ui_MplMainWindow


class DesignerMainWindow(QMainWindow, Ui_MplMainWindow):
    worker = QThread()
    startSimulate = pyqtSignal(list)
    stopSimulate = pyqtSignal()

    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.Cpu1SpinBox.valueChanged.connect(self.data_verification)
        self.Cpu2SpinBox.valueChanged.connect(self.data_verification)
        self.CpucheckBox.toggled.connect(self.disable_cpu_options)
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
        self.StaticAlgorithmRadio.toggled.connect(self.update_algo_list)
        self.DynamicAlgorithmRadio.toggled.connect(self.update_algo_list)
        self.RandomizedDataRadio.toggled.connect(self.disable_prop_options)
        self.CustomDataRadio.toggled.connect(self.disable_prop_options)
        self.LoadPropertiesButton.clicked.connect(self.load_prop_data)
        self.SavePropertiesButton.clicked.connect(self.save_prop_data)
        self.SaveResultsButton.clicked.connect(self.save_result)

        # TODO: Disabled Dynamic Algorithm Selection
        self.DynamicAlgorithmRadio.setEnabled(False)

        self.setWindowTitle("Schedule Simulator v0.0.1")
        self.Cpu1SpinBox.setMaximum(100000)
        self.Cpu2SpinBox.setMaximum(100000)
        self.RunsSpinBox.setMaximum(3)
        self.ProcessesSpinBox.setMaximum(5)
        self.TimeQuantumSpinBox.setMaximum(10)
        self.data_verification()

        self.mplwidget.canvas.ax.set_title("Simulation Test (Example)")
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times")
        self.mplwidget.canvas.ax.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40], label=" Sample Test Plot")
        self.mplwidget.canvas.ax.legend()

        self.processdata = []
        self.result = []
        self.isRunning = False
        self.load = None

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

    def disable_cpu_options(self):
        if self.CpucheckBox.isChecked():
            self.Cpu1SpinBox.setEnabled(False)
            self.Cpu2SpinBox.setEnabled(False)
        else:
            self.Cpu1SpinBox.setEnabled(True)
            self.Cpu2SpinBox.setEnabled(True)

        self.data_verification()

    def generate_random_data(self):
        tempprocessdata = [[self.Cpu1SpinBox.value(), self.Cpu2SpinBox.value(), self.CpucheckBox.isChecked().__int__()]]

        if self.RandomizedDataRadio.isChecked():
            testrun = random.randint(2, self.RunsSpinBox.maximum())
            testprocesses = random.randint(2, self.ProcessesSpinBox.maximum())
            self.RunsSpinBox.setValue(testrun)
            self.ProcessesSpinBox.setValue(testprocesses)
            self.ArrivalTimesValueBox.clear()
            self.BurstTimesValueBox.clear()

            if self.StaticAlgorithmRadio.isChecked():
                quantum = random.randint(1, self.TimeQuantumSpinBox.maximum())
                self.TimeQuantumSpinBox.setValue(quantum)
                temp_min_cpu_speed = None

                if self.CpucheckBox.isChecked():
                    temp_min_cpu_speed = 100000
                elif self.Cpu1SpinBox.value() < self.Cpu2SpinBox.value():
                    temp_min_cpu_speed = self.Cpu1SpinBox.value()
                elif self.Cpu1SpinBox.value() > self.Cpu2SpinBox.value():
                    temp_min_cpu_speed = self.Cpu2SpinBox.value()
                elif self.Cpu1SpinBox.value() == self.Cpu2SpinBox.value():
                    temp_min_cpu_speed = self.Cpu1SpinBox.value()

                for i in range(testrun):
                    temprunsdataRR = []
                    temprunsdataSJF = []

                    for j in range(testprocesses):
                        temp_dataRR = []
                        temp_dataSJF = []
                        process_id = j + 1
                        arrival_time = random.randint(0, 100000)
                        burst_time = random.randint(0, temp_min_cpu_speed)
                        temp_dataRR.extend([process_id, arrival_time, burst_time, 0, burst_time])
                        temp_dataSJF.extend([process_id, arrival_time, burst_time, 0])
                        if self.ArrivalTimesValueBox.toPlainText() != "":
                            if j == 0:
                                self.ArrivalTimesValueBox.setPlainText(self.ArrivalTimesValueBox.toPlainText() + ";"
                                                                       + str(arrival_time))
                                self.BurstTimesValueBox.setPlainText(self.BurstTimesValueBox.toPlainText() + ";"
                                                                     + str(burst_time))
                            else:
                                self.ArrivalTimesValueBox.setPlainText(self.ArrivalTimesValueBox.toPlainText() + ","
                                                                       + str(arrival_time))
                                self.BurstTimesValueBox.setPlainText(self.BurstTimesValueBox.toPlainText() + ","
                                                                     + str(burst_time))
                        else:
                            self.ArrivalTimesValueBox.setPlainText(str(arrival_time))
                            self.BurstTimesValueBox.setPlainText(str(burst_time))
                        temprunsdataRR.append(temp_dataRR)
                        temprunsdataSJF.append(temp_dataSJF)
                    tempprocessdata.append([0, i + 1, temprunsdataRR, quantum])
                    tempprocessdata.append([1, i + 1, temprunsdataSJF, 0])
            elif self.DynamicAlgorithmRadio.isChecked():
                if self.Algorithm2Selector.currentIndex(0):  # Rate Monotonic Scheduling
                    pass
                elif self.Algorithm2Selector.currentIndex(1):  # Earliest Deadline First
                    pass
        elif self.CustomDataRadio.isChecked():
            arrival_time_string = self.ArrivalTimesValueBox.toPlainText()
            arrival_time_string = arrival_time_string.split(";")

            burst_time_string = self.BurstTimesValueBox.toPlainText()
            burst_time_string = burst_time_string.split(";")

            for i in range(self.RunsSpinBox.value()):
                temp_arrival_time_string = arrival_time_string[i].split(",")
                temp_burst_time_string = burst_time_string[i].split(",")
                temprunsdataRR = []
                temprunsdataSJF = []

                for j in range(self.ProcessesSpinBox.value()):
                    temp_dataRR = []
                    temp_dataSJF = []
                    process_id = j + 1
                    arrival_time = int(temp_arrival_time_string[j])
                    burst_time = int(temp_burst_time_string[j])
                    temp_dataRR.extend([process_id, arrival_time, burst_time, 0, burst_time])
                    temp_dataSJF.extend([process_id, arrival_time, burst_time, 0])
                    temprunsdataRR.append(temp_dataRR)
                    temprunsdataSJF.append(temp_dataSJF)
                tempprocessdata.append([0, i + 1, temprunsdataRR, self.TimeQuantumSpinBox.value()])
                tempprocessdata.append([1, i + 1, temprunsdataSJF, 0])

        self.processdata = tempprocessdata
        self.result = []

    def start_simulation(self):
        self.mplwidget.canvas.ax.cla()
        self.mplwidget.canvas.ax.set_title(f"{self.AlgorithmSelector.currentText()} vs "
                                           f"{self.Algorithm2Selector.currentText()} Currently Simulating")
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times")
        self.mplwidget.canvas.ax.plot([0, 1, 2, 3, 4], [random.randint(1, 10),
                                                        random.randint(1, 10), random.randint(1, 10),
                                                        random.randint(1, 10), random.randint(1, 10)],
                                      label="Random Sample Test Plot")
        self.mplwidget.canvas.ax.legend()
        self.mplwidget.canvas.draw()

        if self.isRunning:
            print("Stopping Simulation")
            self.result = []
            self.isRunning = False
            self.StartSimulationButton.setText("Start Simulation")
            self.disable_all_settings()
            self.stopSimulate.emit()
            self.load.blockSignals(True)
            self.load.deleteLater()
            self.worker.quit()
            self.worker.wait()

            self.StartSimulationButton.setText("Start Simulation")

            self.mplwidget.canvas.ax.cla()
            self.mplwidget.canvas.ax.set_title(f"{self.AlgorithmSelector.currentText()} vs "
                                               f"{self.Algorithm2Selector.currentText()} Stopped Simulation Test")
            self.mplwidget.canvas.ax.set_xlabel("Runs")
            self.mplwidget.canvas.ax.set_ylabel("Average waiting times")
            self.mplwidget.canvas.ax.plot([0, 1, 2, 3, 4], [random.randint(1, 10),
                                                            random.randint(1, 10), random.randint(1, 10),
                                                            random.randint(1, 10), random.randint(1, 10)],
                                          label="Random Test Plot")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            return

        self.result = []

        self.load = LoadBalancer(parent=self)
        self.load.moveToThread(self.worker)
        self.load.update_result.connect(self.update_result)
        self.load.finished.connect(self.update_graph)
        self.load.exited.connect(self.load.deleteLater)
        self.worker.start()
        self.isRunning = True
        self.StartSimulationButton.setText("Stop Simulation")
        self.disable_all_settings()
        self.generate_random_data()
        self.startSimulate.emit(self.processdata)
        print("Sending Process Data to Load Balancer :" + self.processdata.__str__())

    def data_verification(self):
        if (self.CpucheckBox.isChecked() or (not self.CpucheckBox.isChecked() and self.Cpu1SpinBox.value() > 0) and
            self.Cpu2SpinBox.value() > 0) and \
                (self.StaticAlgorithmRadio.isChecked() or self.DynamicAlgorithmRadio.isChecked()) and \
                (self.AlgorithmSelector.currentIndex() != -1 or self.Algorithm2Selector.currentIndex() != -1) and \
                (self.CustomDataRadio.isChecked() or self.RandomizedDataRadio.isChecked()) and \
                (self.AlgorithmSelector.currentIndex() != self.Algorithm2Selector.currentIndex() and
                 self.arrival_burst_time_data_verification() and
                 (self.RandomizedDataRadio.isChecked() or self.RunsSpinBox.value() > 1 and
                  self.ProcessesSpinBox.value() > 1 and
                  self.RandomizedDataRadio.isChecked() or self.TimeQuantumSpinBox.value() > 0) and
                 (self.RandomizedDataRadio.isChecked() or self.ArrivalTimesValueBox.toPlainText() != "" and
                  self.BurstTimesValueBox.toPlainText() != "")):
            self.StartSimulationButton.setEnabled(True)
            self.StartSimulationButton.setStyleSheet("background-color: rgb(255, 0, 0);color: rgb(255, 255, 255);")
        else:
            self.StartSimulationButton.setDisabled(True)
            self.StartSimulationButton.setStyleSheet("")

    def arrival_burst_time_data_verification(self):
        if self.RandomizedDataRadio.isChecked():
            return True

        arrival_time_string = self.ArrivalTimesValueBox.toPlainText()
        arrival_time_string = arrival_time_string.split(";")

        burst_time_string = self.BurstTimesValueBox.toPlainText()
        burst_time_string = burst_time_string.split(";")

        if len(arrival_time_string) != self.RunsSpinBox.value() or len(burst_time_string) != self.RunsSpinBox.value():
            return False

        lowest_cpu_speed = None

        if self.Cpu1SpinBox.value() < self.Cpu2SpinBox.value():
            lowest_cpu_speed = self.Cpu1SpinBox.value()
        elif self.Cpu1SpinBox.value() > self.Cpu2SpinBox.value():
            lowest_cpu_speed = self.Cpu2SpinBox.value()
        elif self.Cpu1SpinBox.value() == self.Cpu2SpinBox.value():
            lowest_cpu_speed = self.Cpu1SpinBox.value()

        for i in range(self.RunsSpinBox.value()):
            arrival_time_string[i] = arrival_time_string[i].split(",")
            burst_time_string[i] = burst_time_string[i].split(",")

            for j in range(len(arrival_time_string[i])):
                if len(arrival_time_string[i]) != self.ProcessesSpinBox.value() or arrival_time_string[i][j] == "" \
                        or not arrival_time_string[i][j].isdigit():
                    return False

            for j in range(len(burst_time_string[i])):
                if len(burst_time_string[i]) != self.ProcessesSpinBox.value() or burst_time_string[i][j] == "" \
                        or not burst_time_string[i][j].isdigit() \
                        or (not self.CpucheckBox.isChecked() and int(burst_time_string[i][j]) > lowest_cpu_speed):
                    return False
        return True

    def load_prop_data(self):
        data = QFileDialog(self)
        data.setWindowTitle("Open Properties Save File")
        data.setFileMode(QFileDialog.ExistingFile)
        data.setViewMode(QFileDialog.List)
        data.setNameFilter(self.tr("Properties Save File (*.sav)"))
        directory = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)
        data.setDirectory(directory[0])
        if data.exec():
            filename = data.selectedFiles()
            datafile = open(filename[0], "r")
            if not datafile.errors:
                datafile.close()
                message = QMessageBox(self)
                message.setText(f"Error opening File: {filename}")
                message.setWindowTitle(self.windowTitle())
                message.setIcon(QMessageBox.Warning)
                message.setStandardButtons(QMessageBox.Ok)
                message.exec()
                return

            jsondata = json.loads(datafile.read())
            datafile.close()

            if "cpumode" in jsondata:
                if int(jsondata["cpumode"]) == 0:
                    self.CpucheckBox.setChecked(False)
                    if "cpudata" in jsondata:
                        if "cpu1" in jsondata["cpudata"]:
                            self.Cpu1SpinBox.setValue(int(jsondata["cpudata"]["cpu1"]))
                        else:
                            self.Cpu1SpinBox.setValue(0)
                        if "cpu2" in jsondata["cpudata"]:
                            self.Cpu2SpinBox.setValue(int(jsondata["cpudata"]["cpu2"]))
                        else:
                            self.Cpu2SpinBox.setValue(0)
                    else:
                        self.Cpu1SpinBox.setValue(0)
                        self.Cpu2SpinBox.setValue(0)
                elif int(jsondata["cpumode"]) == 1:
                    self.CpucheckBox.setChecked(True)
                    self.Cpu1SpinBox.setValue(0)
                    self.Cpu2SpinBox.setValue(0)
            else:
                self.CpucheckBox.setChecked(False)
                self.Cpu1SpinBox.setValue(0)
                self.Cpu2SpinBox.setValue(0)

            if "algorithmtype" in jsondata:
                if int(jsondata["algorithmtype"]) == 0:
                    self.StaticAlgorithmRadio.setChecked(True)
                elif int(jsondata["algorithmtype"]) == 1:
                    self.DynamicAlgorithmRadio.setChecked(True)
            else:
                self.StaticAlgorithmRadio.autoExclusive(False)
                self.DynamicAlgorithmRadio.autoExclusive(False)
                self.StaticAlgorithmRadio.setChecked(False)
                self.DynamicAlgorithmRadio.setChecked(False)
                self.StaticAlgorithmRadio.autoExclusive(True)
                self.DynamicAlgorithmRadio.autoExclusive(True)

            if "algorithm1" in jsondata:
                self.AlgorithmSelector.setCurrentIndex(int(jsondata["algorithm1"]))
            else:
                self.AlgorithmSelector.setCurrentIndex(0)
            if "algorithm2" in jsondata:
                self.Algorithm2Selector.setCurrentIndex(int(jsondata["algorithm2"]))
            else:
                self.Algorithm2Selector.setCurrentIndex(0)

            if "simulationconfig" in jsondata:
                if int(jsondata["simulationconfig"]) == 0:
                    self.CustomDataRadio.setChecked(True)
                    if "data" in jsondata:
                        if "runs" in jsondata["data"]:
                            self.RunsSpinBox.setValue(int(jsondata["data"]["runs"]))
                        else:
                            self.RunsSpinBox.setValue(0)
                        if "processes" in jsondata["data"]:
                            self.ProcessesSpinBox.setValue(int(jsondata["data"]["processes"]))
                        else:
                            self.ProcessesSpinBox.setValue(0)
                        if "timequantum" in jsondata["data"]:
                            self.TimeQuantumSpinBox.setValue(int(jsondata["data"]["timequantum"]))
                        else:
                            self.TimeQuantumSpinBox.setValue(0)
                        if "arrivaltimes" in jsondata["data"]:
                            self.ArrivalTimesValueBox.setPlainText(str(jsondata["data"]["arrivaltimes"]))
                        else:
                            self.ArrivalTimesValueBox.setValue(0)
                        if "burstimes" in jsondata["data"]:
                            self.BurstTimesValueBox.setPlainText(str(jsondata["data"]["burstimes"]))
                        else:
                            self.BurstTimesValueBox.setValue(0)
                    else:
                        self.RunsSpinBox.setValue(0)
                        self.ProcessesSpinBox.setValue(0)
                        self.TimeQuantumSpinBox.setValue(0)
                        self.ArrivalTimesValueBox.clear()
                        self.BurstTimesValueBox.clear()
                elif int(jsondata["simulationconfig"]) == 1:
                    self.RandomizedDataRadio.setChecked(True)
                    self.RunsSpinBox.setValue(0)
                    self.ProcessesSpinBox.setValue(0)
                    self.TimeQuantumSpinBox.setValue(0)
                    self.ArrivalTimesValueBox.clear()
                    self.BurstTimesValueBox.clear()
            else:
                self.CustomDataRadio.setAutoExclusive(False)
                self.RandomizedDataRadio.setAutoExclusive(False)
                self.CustomDataRadio.setChecked(False)
                self.RandomizedDataRadio.setChecked(False)
                self.CustomDataRadio.setAutoExclusive(True)
                self.RandomizedDataRadio.setAutoExclusive(True)
                self.RunsSpinBox.setValue(0)
                self.ProcessesSpinBox.setValue(0)
                self.TimeQuantumSpinBox.setValue(0)
                self.ArrivalTimesValueBox.clear()
                self.BurstTimesValueBox.clear()

            message = QMessageBox()
            message.setWindowTitle(self.windowTitle())
            message.setIcon(QMessageBox.Information)
            message.setText(f"Successfuly load Properties file '{filename[0]}'")
            message.exec()

    def save_prop_data(self):
        filename = QFileDialog(self)
        filename.setWindowTitle("Save Properties Save File")
        filename.setFileMode(QFileDialog.ExistingFile)
        filename.setViewMode(QFileDialog.List)
        filename.setAcceptMode(QFileDialog.AcceptSave)
        filename.setNameFilters([self.tr("Properties Save File (*.sav)"),
                                 self.tr("Any Files (*)")])
        directory = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)
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
                    temp = {"cpumode": self.CpucheckBox.isChecked().__int__()}
                    if self.CpucheckBox.isChecked():
                        temp["cpudata"] = None
                    else:
                        temp["cpudata"] = {
                            "cpu1": self.Cpu1SpinBox.value(),
                            "cpu2": self.Cpu2SpinBox.value()
                        }
                    if self.StaticAlgorithmRadio.isChecked() and not self.DynamicAlgorithmRadio.isChecked():
                        temp["algorithmtype"] = 0
                    else:
                        temp["algorithmtype"] = 1

                    temp["algorithm1"] = self.AlgorithmSelector.currentIndex()
                    temp["algorithm2"] = self.Algorithm2Selector.currentIndex()

                    if self.CustomDataRadio.isChecked() and not self.RandomizedDataRadio.isChecked():
                        temp["simulationconfig"] = 0
                        temp["data"] = {
                            "runs": self.RunsSpinBox.value(),
                            "processes": self.ProcessesSpinBox.value(),
                            "timequantum": self.TimeQuantumSpinBox.value(),
                            "arrivaltimes": self.ArrivalTimesValueBox.toPlainText(),
                            "burstimes": self.BurstTimesValueBox.toPlainText()
                        }
                    else:
                        temp["simulationconfig"] = 1
                        temp["data"] = None
                    json.dump(temp, json_file, indent=4)
                print(f"Successfully saved file at {datafilename}")
                message = QMessageBox()
                message.setWindowTitle(self.windowTitle())
                message.setIcon(QMessageBox.Information)
                message.setText(f"Successfully saved file at {datafilename}")
                message.exec()
            except IOError:
                print(IOError)
                print(f"File '{datafilename}' is currently in use or not accessible")
                message = QMessageBox()
                message.setWindowTitle(self.windowTitle())
                message.setIcon(QMessageBox.Warning)
                message.setText(f"File '{datafilename}' is currently in use or not accessible")
                message.exec()

    def update_graph(self):
        result = self.result
        runsRR = []
        runsSJF = []
        resultRR = []
        resultSJF = []

        result.sort(key=lambda x: x[1])

        for i in range(len(result)):
            if result[i][0] == 0:
                resultRR.append(result[i][2])
                runsRR.append(result[i][1])
            if result[i][0] == 1:
                resultSJF.append(result[i][2])
                runsSJF.append(result[i][1])

        print("Emitted from Worker Thread")
        print("Showing Results on Main")
        print(f"From Received Result: {self.result}")
        print(f"Round Robin: {runsRR}, {resultRR}")
        print(f"Shortest Job First: {runsSJF}, {resultSJF}")

        self.mplwidget.canvas.ax.cla()
        self.mplwidget.canvas.ax.set_title(f"{self.AlgorithmSelector.currentText()} vs "
                                           f"{self.Algorithm2Selector.currentText()} Simulation Test Result")
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times")

        self.mplwidget.canvas.ax.plot(runsRR, resultRR, label="Round Robin")
        self.mplwidget.canvas.ax.legend()
        self.mplwidget.canvas.draw()
        self.mplwidget.canvas.ax.plot(runsSJF, resultSJF, label="Shortest Job First")
        self.mplwidget.canvas.ax.legend()
        self.mplwidget.canvas.draw()

        self.isRunning = False
        self.result = []
        self.StartSimulationButton.setText("Start Simulation")
        self.disable_all_settings()
        self.load.blockSignals(True)
        self.load.deleteLater()
        self.worker.quit()
        self.worker.wait()

    def update_result(self, result):
        self.result.append(result)
        print(f'Updating Result : {self.result}')

    def disable_all_settings(self):
        if self.isRunning:
            self.CpuGroup.setEnabled(False)
            self.StaticDynamicGroup.setEnabled(False)
            self.AlgorithmSelector.setEnabled(False)
            self.Algorithm2Selector.setEnabled(False)
            self.CustomRandomGroup.setEnabled(False)
            self.RunsGroup.setEnabled(False)
            self.ProcessesGroup.setEnabled(False)
            self.TimeQuantumGroup.setEnabled(False)
            self.ArrivalGroup.setEnabled(False)
            self.BurstGroup.setEnabled(False)
            self.LoadPropertiesButton.setEnabled(False)
            self.SavePropertiesButton.setEnabled(False)
            self.SaveResultsButton.setEnabled(False)
        else:
            self.CpuGroup.setEnabled(True)
            self.StaticDynamicGroup.setEnabled(True)
            self.AlgorithmSelector.setEnabled(True)
            self.Algorithm2Selector.setEnabled(True)
            self.CustomRandomGroup.setEnabled(True)
            self.LoadPropertiesButton.setEnabled(True)
            self.SavePropertiesButton.setEnabled(True)
            self.SaveResultsButton.setEnabled(True)
            self.disable_prop_options()

    # TODO: Needs to add result.
    def save_result(self):
        filename = QFileDialog(self)
        filename.setWindowTitle("Save Results Image File")
        filename.setFileMode(QFileDialog.ExistingFile)
        filename.setViewMode(QFileDialog.List)
        filename.setAcceptMode(QFileDialog.AcceptSave)
        filename.setNameFilters([self.tr("PNG (*.png)"),
                                 self.tr("PDF (*.pdf)"),
                                 self.tr("SVG (*.svg)"),
                                 self.tr("JPEG (*.jpg;*.jpeg)")])
        directory = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)
        filename.setDirectory(directory[0])

        if filename.exec():
            datafilename = filename.selectedFiles()[0]
            try:
                createfile = open(datafilename, 'x')
                createfile.close()
            except IOError:
                print("File is already created!")

            try:
                self.mplwidget.canvas.fig.savefig(datafilename)
            except IOError:
                print(IOError)
                print(f"File '{datafilename}' is currently in use or not accessible")
            finally:
                message = QMessageBox(self)
                message.setText(f"Successfully saved Image File at '{datafilename}'")
                message.setWindowTitle(self.windowTitle())
                message.setIcon(QMessageBox.Information)
                message.setStandardButtons(QMessageBox.Ok)
                message.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
