import json
import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from source.Library.Common.LoadBalancer import LoadBalancer
from source.Library.UI.schedulesim_ui import UiMplMainWindow


class DesignerMainWindow(QMainWindow, UiMplMainWindow):
    worker = QThread()
    startSimulate = pyqtSignal(list)
    stopSimulate = pyqtSignal()

    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupui(self)

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
        self.DynamicAlgorithmRadio.setHidden(True)

        self.setWindowTitle("Schedule Simulator v0.0.1")
        self.Cpu1SpinBox.setMaximum(100000)
        self.Cpu2SpinBox.setMaximum(100000)
        self.RunsSpinBox.setMaximum(5)
        self.ProcessesSpinBox.setMaximum(10)
        self.TimeQuantumSpinBox.setMaximum(10)
        self.arrival_error = False
        self.burst_error = False
        self.data_verification()

        self.mplwidget.canvas.ax.set_title("Simulation Test (Example)")
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times (ms)")
        self.mplwidget.canvas.ax.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40], label=" Sample Test Plot")
        self.mplwidget.canvas.ax.legend()

        self.temp_cpu2_save_prev = 0
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
            self.temp_cpu2_save_prev = self.Cpu2SpinBox.value()
            self.Cpu2SpinBox.setValue(0)
            self.Cpu2SpinBox.setEnabled(False)
            self.Cpu2String.setEnabled(False)
        else:
            self.Cpu2SpinBox.setValue(self.temp_cpu2_save_prev)
            self.Cpu2SpinBox.setEnabled(True)
            self.Cpu2String.setEnabled(True)

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
                fastest_cpu_speed = None

                if self.CpucheckBox.isChecked():
                    fastest_cpu_speed = self.Cpu1SpinBox.value()
                elif self.Cpu1SpinBox.value() < self.Cpu2SpinBox.value():
                    fastest_cpu_speed = self.Cpu1SpinBox.value()
                elif self.Cpu1SpinBox.value() > self.Cpu2SpinBox.value():
                    fastest_cpu_speed = self.Cpu2SpinBox.value()
                elif self.Cpu1SpinBox.value() == self.Cpu2SpinBox.value():
                    fastest_cpu_speed = self.Cpu1SpinBox.value()

                for i in range(testrun):
                    temprunsdataRR = []
                    temprunsdataSJF = []

                    for j in range(testprocesses):
                        temp_dataRR = []
                        temp_dataSJF = []
                        process_id = j + 1
                        arrival_time = random.randint(0, int(float(fastest_cpu_speed) * 1.25))
                        burst_time = random.randint(0, fastest_cpu_speed)
                        temp_dataRR.extend([process_id, arrival_time, burst_time, 0, burst_time])
                        temp_dataSJF.extend([process_id, arrival_time, burst_time, 0])
                        if self.ArrivalTimesValueBox.toPlainText() != "":
                            if j == 0:
                                self.ArrivalTimesValueBox.setPlainText(self.ArrivalTimesValueBox.toPlainText() + "\n\n"
                                                                       + str(arrival_time))
                                self.BurstTimesValueBox.setPlainText(self.BurstTimesValueBox.toPlainText() + "\n\n"
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
            arrival_time_string = arrival_time_string.split("\n\n")

            burst_time_string = self.BurstTimesValueBox.toPlainText()
            burst_time_string = burst_time_string.split("\n\n")

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
        self.mplwidget.canvas.ax.set_ylabel("Average waiting times (ms)")
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
            self.mplwidget.canvas.ax.set_ylabel("Average waiting times (ms)")
            self.mplwidget.canvas.ax.plot([0, 1, 2, 3, 4], [random.randint(1, 10),
                                                            random.randint(1, 10), random.randint(1, 10),
                                                            random.randint(1, 10), random.randint(1, 10)],
                                          label="Random Test Plot")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            return

        self.result = []
        self.consoleplainTextEdit.clear()

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
            self.ArrivalTimesString.setStyleSheet("")
            self.BurstTimesString.setStyleSheet("")
        else:
            self.StartSimulationButton.setDisabled(True)
            self.StartSimulationButton.setStyleSheet("")
            if self.ArrivalTimesValueBox.toPlainText() != "":
                if self.arrival_error:
                    self.ArrivalTimesString.setStyleSheet("color: rgb(255, 0, 0);")
                else:
                    self.ArrivalTimesString.setStyleSheet("")
            if self.BurstTimesValueBox.toPlainText() != "":
                if self.burst_error:
                    self.BurstTimesString.setStyleSheet("color: rgb(255, 0, 0);")
                else:
                    self.BurstTimesString.setStyleSheet("")

    def arrival_burst_time_data_verification(self):
        checkok = True
        self.arrival_error = False
        self.burst_error = False
        if self.RandomizedDataRadio.isChecked():
            return True

        fastest_cpu_speed = None

        if not self.CpucheckBox.isChecked():
            if self.Cpu1SpinBox.value() < self.Cpu2SpinBox.value():
                fastest_cpu_speed = self.Cpu1SpinBox.value()
            elif self.Cpu1SpinBox.value() > self.Cpu2SpinBox.value():
                fastest_cpu_speed = self.Cpu2SpinBox.value()
            elif self.Cpu1SpinBox.value() == self.Cpu2SpinBox.value():
                fastest_cpu_speed = self.Cpu1SpinBox.value()
        else:
            fastest_cpu_speed = self.Cpu1SpinBox.value()

        arrival_time_string = self.ArrivalTimesValueBox.toPlainText()
        arrival_time_string = arrival_time_string.split("\n\n")

        burst_time_string = self.BurstTimesValueBox.toPlainText()
        burst_time_string = burst_time_string.split("\n\n")

        if len(arrival_time_string) != self.RunsSpinBox.value() or len(burst_time_string) != self.RunsSpinBox.value():
            if len(arrival_time_string) != self.RunsSpinBox.value():
                if len(arrival_time_string):
                    self.arrival_error = True
                else:
                    self.arrival_error = False
            else:
                for i in range(self.RunsSpinBox.value()):
                    arrival_time_string[i] = arrival_time_string[i].split(",")

                    for j in range(len(arrival_time_string[i])):
                        if len(arrival_time_string[i]) != self.ProcessesSpinBox.value() or arrival_time_string[i][
                            j] == "" \
                                or not arrival_time_string[i][j].isdigit():
                            self.arrival_error = True
                            break

            if len(burst_time_string) != self.RunsSpinBox.value():
                if len(burst_time_string):
                    self.burst_error = True
                else:
                    self.burst_error = False
            else:
                for i in range(self.RunsSpinBox.value()):
                    burst_time_string[i] = burst_time_string[i].split(",")

                    for j in range(len(burst_time_string[i])):
                        if len(burst_time_string[i]) != self.ProcessesSpinBox.value() or burst_time_string[i][
                            j] == "" \
                                or not burst_time_string[i][j].isdigit() \
                                or int(burst_time_string[i][j]) > fastest_cpu_speed:
                            self.burst_error = True
                            break
            return False

        for i in range(self.RunsSpinBox.value()):
            arrival_time_string[i] = arrival_time_string[i].split(",")
            burst_time_string[i] = burst_time_string[i].split(",")

            for j in range(len(arrival_time_string[i])):
                if len(arrival_time_string[i]) != self.ProcessesSpinBox.value() or arrival_time_string[i][j] == "" \
                        or not arrival_time_string[i][j].isdigit():
                    self.arrival_error = True
                    checkok = False
                    break

            for j in range(len(burst_time_string[i])):
                if len(burst_time_string[i]) != self.ProcessesSpinBox.value() or burst_time_string[i][j] == "" \
                        or not burst_time_string[i][j].isdigit() \
                        or int(burst_time_string[i][j]) > fastest_cpu_speed:
                    self.burst_error = True
                    checkok = False
                    break

        if not checkok:
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
        directory = QStandardPaths.standardLocations(QStandardPaths.DownloadLocation)
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
        waitingRR = []
        waitingRR_cpu2 = []
        waitingSJF = []
        waitingSJF_cpu2 = []
        turnaroundRR = []
        turnaroundRR_cpu2 = []
        turnaroundSJF = []
        turnaroundSJF_cpu2 = []

        result.sort(key=lambda x: x[2])

        for i in range(len(result)):
            if result[i][0] == 0:
                turnaroundRR.append(result[i][4])
                waitingRR.append(result[i][3])
                runsRR.append(result[i][2])
                if result[i][1] == 1:
                    turnaroundRR_cpu2.append(result[i][6])
                    waitingRR_cpu2.append(result[i][5])
            if result[i][0] == 1:
                turnaroundSJF.append(result[i][4])
                waitingSJF.append(result[i][3])
                runsSJF.append(result[i][2])
                if result[i][1] == 1:
                    turnaroundSJF_cpu2.append(result[i][6])
                    waitingSJF_cpu2.append(result[i][5])

        print("Emitted from Worker Thread")
        print("Showing Results on Main")
        print(f"From Received Result: {self.result}")
        self.consoleplainTextEdit.appendPlainText("Results:\n\n")
        self.mplwidget.canvas.ax.cla()
        self.mplwidget.canvas.ax.set_title(f"{self.AlgorithmSelector.currentText()} vs "
                                           f"{self.Algorithm2Selector.currentText()} Simulation Test Result")
        self.mplwidget.canvas.ax.set_xlabel("Runs")
        self.mplwidget.canvas.ax.set_ylabel("Average time (ms)")
        if self.CpucheckBox.isChecked():
            print(f"Round Robin: {runsRR}, {waitingRR}, {turnaroundRR}")
            print(f"Shortest Job First: {runsSJF}, {waitingSJF}, {turnaroundSJF}")

            self.consoleplainTextEdit.appendPlainText(f"Round Robin:\n\n"
                                                      f"Run     Average Waiting Time        Average Turnaround Time")
            temp_truns = 0.00
            temp_tat = 0.00
            temp_wt = 0.00
            for i in range(len(runsRR)):
                waitingRR[i] = round(float(waitingRR[i]), 2)
                turnaroundRR[i] = round(float(turnaroundRR[i]), 2)
                self.consoleplainTextEdit.appendPlainText(f"{runsRR[i]}                  {waitingRR[i]} ms    "
                                                          f"                               {turnaroundRR[i]} ms")
                temp_truns += runsRR[i]
                temp_wt += waitingRR[i]
                temp_tat += turnaroundRR[i]
            temp_tat = temp_tat / temp_truns
            temp_wt = temp_wt / temp_truns
            temp_tat = round(temp_tat, 2)
            temp_wt = round(temp_wt, 2)
            # self.consoleplainTextEdit.appendPlainText(f"\nAverage Turnaround Time: {temp_tat} ms\n"
                                                      # f"Average Waiting Time: {temp_wt} ms\n")

            self.consoleplainTextEdit.appendPlainText(f"\nShortest Job First:\n\n"
                                                      f"Run     Average Waiting Time        Average Turnaround Time")
            temp_truns = 0.00
            temp_tat = 0.00
            temp_wt = 0.00
            for i in range(len(runsSJF)):
                waitingSJF[i] = round(float(waitingSJF[i]), 2)
                turnaroundSJF[i] = round(float(turnaroundSJF[i]), 2)
                self.consoleplainTextEdit.appendPlainText(f"{runsSJF[i]}                 {waitingSJF[i]} ms   "
                                                          f"                               {turnaroundSJF[i]} ms")
                temp_truns += runsSJF[i]
                temp_wt += waitingSJF[i]
                temp_tat += turnaroundSJF[i]
            temp_tat = temp_tat / temp_truns
            temp_wt = temp_wt / temp_truns
            temp_tat = round(temp_tat, 2)
            temp_wt = round(temp_wt, 2)
            # self.consoleplainTextEdit.appendPlainText(f"\nAverage Turnaround Time: {temp_tat} ms\n"
                                                      # f"Average Waiting Time: {temp_wt} ms\n")

            self.mplwidget.canvas.ax.plot(runsRR, waitingRR, label="Round Robin (waiting time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsSJF, waitingSJF, label="Shortest Job First (waiting time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsRR, turnaroundRR, label="Round Robin (turnaround time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsSJF, turnaroundSJF, label="Shortest Job First (turnaround time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
        else:
            print(f"Round Robin CPU 1: {runsRR}, {waitingRR}, {turnaroundRR}")
            print(f"Round Robin CPU 2: {runsRR}, {waitingRR_cpu2}, {turnaroundRR_cpu2}")
            print(f"Shortest Job First CPU 1: {runsSJF}, {waitingSJF}, {turnaroundSJF}")
            print(f"Shortest Job First CPU 2: {runsSJF}, {waitingSJF_cpu2}, {turnaroundSJF_cpu2}")

            self.consoleplainTextEdit.appendPlainText(f"Round Robin CPU 1:\n\n"
                                                      f"Run     Waiting Time        Turnaround Time")
            temp_truns = 0.00
            temp_tat = 0.00
            temp_wt = 0.00
            for i in range(len(runsRR)):
                waitingRR[i] = round(waitingRR[i], 2)
                turnaroundRR[i] = round(turnaroundRR[i], 2)
                self.consoleplainTextEdit.appendPlainText(f"{runsRR[i]}         {waitingRR[i]} ms    "
                                                          f"           {turnaroundRR[i]} ms")
                temp_truns += runsRR[i]
                temp_wt += waitingRR[i]
                temp_tat += turnaroundRR[i]
            temp_tat = temp_tat / temp_truns
            temp_wt = temp_wt / temp_truns
            temp_tat = round(temp_tat, 2)
            temp_wt = round(temp_wt, 2)
            # self.consoleplainTextEdit.appendPlainText(f"\nAverage Turnaround Time: {temp_tat} ms\n"
                                                      # f"Average Waiting Time: {temp_wt} ms\n")

            self.consoleplainTextEdit.appendPlainText(f"\nRound Robin CPU 2:\n\n"
                                                      f"Run     Waiting Time        Turnaround Time")
            temp_truns = 0.00
            temp_tat = 0.00
            temp_wt = 0.00
            for i in range(len(runsRR)):
                waitingRR_cpu2[i] = round(waitingRR_cpu2[i], 2)
                turnaroundRR_cpu2[i] = round(turnaroundRR_cpu2[i], 2)
                self.consoleplainTextEdit.appendPlainText(f"{runsRR[i]}             {waitingRR_cpu2[i]} ms    "
                                                          f"           {turnaroundRR_cpu2[i]} ms")
                temp_truns += runsRR[i]
                temp_wt += waitingRR_cpu2[i]
                temp_tat += turnaroundRR_cpu2[i]
            temp_tat = temp_tat / temp_truns
            temp_wt = temp_wt / temp_truns
            temp_tat = round(temp_tat, 2)
            temp_wt = round(temp_wt, 2)
            # self.consoleplainTextEdit.appendPlainText(f"\nAverage Turnaround Time: {temp_tat} ms\n"
                                                      # f"Average Waiting Time: {temp_wt} ms\n")

            self.consoleplainTextEdit.appendPlainText(f"\nRound Robin Both CPU:\n\n"
                                                      f"Run" + "Average Waiting Time".center(25)
                                                      + "Average Turnaround Time".center(25))
            for i in range(len(runsRR)):
                self.consoleplainTextEdit.appendPlainText(
                    f" {runsRR[i]}"
                    f"{format(str(round(waitingRR[i] + waitingRR_cpu2[i], 2)) + ' ms').center(40)}"
                    f"{format(str(round(turnaroundRR[i] + turnaroundRR_cpu2[i], 2)) + ' ms').center(40)}"
                )

            self.consoleplainTextEdit.appendPlainText(f"\nShortest Job First CPU 1:\n\n"
                                                      f"Run     Waiting Time        Turnaround Time")
            temp_truns = 0.00
            temp_tat = 0.00
            temp_wt = 0.00
            for i in range(len(runsSJF)):
                waitingSJF[i] = round(waitingSJF[i], 2)
                turnaroundSJF[i] = round(turnaroundSJF[i], 2)
                self.consoleplainTextEdit.appendPlainText(f"{runsSJF[i]}             {waitingSJF[i]} ms    "
                                                          f"           {turnaroundSJF[i]} ms")
                temp_truns += runsSJF[i]
                temp_wt += waitingSJF[i]
                temp_tat += turnaroundSJF[i]
            temp_tat = temp_tat / temp_truns
            temp_wt = temp_wt / temp_truns
            temp_tat = round(temp_tat, 2)
            temp_wt = round(temp_wt, 2)
            # self.consoleplainTextEdit.appendPlainText(f"\nAverage Turnaround Time: {temp_tat} ms\n"
                                                     # f"Average Waiting Time: {temp_wt} ms\n")

            self.consoleplainTextEdit.appendPlainText(f"\nShortest Job First CPU 2:\n\n"
                                                      f"Run     Waiting Time        Turnaround Time")
            temp_truns = 0.00
            temp_tat = 0.00
            temp_wt = 0.00
            for i in range(len(runsSJF)):
                waitingSJF_cpu2[i] = round(waitingSJF_cpu2[i], 2)
                turnaroundSJF_cpu2[i] = round(turnaroundSJF_cpu2[i], 2)
                self.consoleplainTextEdit.appendPlainText(
                    f"{runsSJF[i]}             {waitingSJF_cpu2[i]} ms    "
                    f"           {turnaroundSJF_cpu2[i]} ms")
                temp_truns += runsSJF[i]
                temp_wt += waitingSJF_cpu2[i]
                temp_tat += turnaroundSJF_cpu2[i]
            temp_tat = temp_tat / temp_truns
            temp_wt = temp_wt / temp_truns
            temp_tat = round(temp_tat, 2)
            temp_wt = round(temp_wt, 2)
            # self.consoleplainTextEdit.appendPlainText(f"\nAverage Turnaround Time: {temp_tat} ms\n"
                                                      # f"Average Waiting Time: {temp_wt} ms\n")

            self.consoleplainTextEdit.appendPlainText(f"\nShortest Job First Both CPU:\n\n"
                                                      f"Run" + "Average Waiting Time".center(25)
                                                      + "Average Turnaround Time".center(25))
            for i in range(len(runsRR)):
                self.consoleplainTextEdit.appendPlainText(
                    f" {runsRR[i]}"
                    f"{format(str(round(waitingSJF[i] + waitingSJF_cpu2[i], 2)) + ' ms').center(40)}"
                    f"{format(str(round(turnaroundSJF[i] + turnaroundSJF_cpu2[i], 2)) + ' ms').center(40)}"
                )

            self.mplwidget.canvas.ax.plot(runsRR, waitingRR, label="Round Robin CPU 1 (waiting time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsRR, waitingRR_cpu2, label="Round Robin CPU 2 (waiting time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsSJF, waitingSJF, label="Shortest Job First CPU 1 (waiting time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsSJF, waitingSJF_cpu2, label="Shortest Job First CPU 2 (waiting time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsRR, turnaroundRR, label="Round Robin CPU 1 (turnaround time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsRR, turnaroundRR_cpu2, label="Round Robin CPU 2 (turnaround time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsSJF, turnaroundSJF, label="Shortest Job First CPU 2(turnaround time)")
            self.mplwidget.canvas.ax.legend()
            self.mplwidget.canvas.draw()
            self.mplwidget.canvas.ax.plot(runsSJF, turnaroundSJF_cpu2,
                                          label="Shortest Job First CPU 2 (turnaround time)")
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
            directory = filename.directory()
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

        filename = QFileDialog(self)
        filename.setWindowTitle("Save Results text File")
        filename.setFileMode(QFileDialog.ExistingFile)
        filename.setViewMode(QFileDialog.List)
        filename.setAcceptMode(QFileDialog.AcceptSave)
        filename.setNameFilters([self.tr("text (*.txt)")])
        filename.setDirectory(directory[0])

        if filename.exec():
            datafilename = filename.selectedFiles()[0]
            directory = filename.directory()
            try:
                createfile = open(datafilename, 'x')
                createfile.close()
            except IOError:
                print("File is already created!")

            try:
                editfile = open(datafilename, 'w')
                editfile.write(self.consoleplainTextEdit.toPlainText())
                editfile.close()
            except IOError:
                print(IOError)
                print(f"File '{datafilename}' is currently in use or not accessible")
            finally:
                message = QMessageBox(self)
                message.setText(f"Successfully saved text File at '{datafilename}'")
                message.setWindowTitle(self.windowTitle())
                message.setIcon(QMessageBox.Information)
                message.setStandardButtons(QMessageBox.Ok)
                message.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
