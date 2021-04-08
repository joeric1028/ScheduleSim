import queue
import threading
import time

from PyQt5.QtCore import *

from source.Library.Common.ThreadWorker import ThreadWorker


class LoadBalancer(QObject):
    update_result = pyqtSignal(list)
    finished = pyqtSignal()
    exited = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = []
        self.isRunning = False
        self.stopRunning = False
        self.load_balance_process = None
        parent.startSimulate.connect(self.start_thread_process)
        parent.stopSimulate.connect(self.stop)

    def __del__(self):
        print("Deleting Load Balancer object")
        del self.results
        del self.load_balance_process

    # Main task function
    def _main_process(self, item_queue, result_queue, otherargs):
        # Go through each link in the array passed in.
        while not item_queue.empty():
            if self.stopRunning:
                return

            # Get the next item in the queue
            item = item_queue.get()
            tempWaitingRRcpu1 = 0
            tempWaitingRRcpu2 = 0
            tempWaitingSJFcpu1 = 0
            tempWaitingSJFcpu2 = 0

            cpu1, cpu2, process_data = self._load_balance(item[2], otherargs[0][0][0], otherargs[0][0][1])
            tempworkercpu1 = ThreadWorker([item[0], item[1], cpu1, item[3]])
            tempworkercpu2 = ThreadWorker([item[0], item[1], cpu2, item[3]])

            if tempworkercpu1.waitingRR is not None:
                tempWaitingRRcpu1 = tempWaitingRRcpu1 + tempworkercpu1.waitingRR
            if tempworkercpu1.waitingSJF is not None:
                tempWaitingSJFcpu1 = tempWaitingSJFcpu1 + tempworkercpu1.waitingSJF

            if tempworkercpu2.waitingRR is not None:
                tempWaitingRRcpu2 = tempWaitingRRcpu2 + tempworkercpu2.waitingRR
            if tempworkercpu2.waitingSJF is not None:
                tempWaitingSJFcpu2 = tempWaitingSJFcpu2 + tempworkercpu2.waitingSJF

            while len(process_data) != 0:
                cpu_1, cpu_2, processes_data = self._load_balance(process_data, 15, 10)
                tempworkercpu1 = ThreadWorker([item[0], item[1], cpu_1, item[3]])
                tempworkercpu2 = ThreadWorker([item[0], item[1], cpu_2, item[3]])
                if self.stopRunning:
                    return

                if tempworkercpu1.waitingRR is not None:
                    tempWaitingRRcpu1 = tempWaitingRRcpu1 + tempworkercpu1.waitingRR
                if tempworkercpu1.waitingSJF is not None:
                    tempWaitingSJFcpu1 = tempWaitingSJFcpu1 + tempworkercpu1.waitingSJF

                if tempworkercpu2.waitingRR is not None:
                    tempWaitingRRcpu2 = tempWaitingRRcpu2 + tempworkercpu2.waitingRR
                if tempworkercpu2.waitingSJF is not None:
                    tempWaitingSJFcpu2 = tempWaitingSJFcpu2 + tempworkercpu2.waitingSJF

            if tempworkercpu1.waitingRR is not None:
                result_queue.put([tempworkercpu1.algo, tempworkercpu1.runs, 0, tempWaitingRRcpu1])
                self.update_result.emit([tempworkercpu1.algo, tempworkercpu1.runs, 0, tempWaitingRRcpu1])
                result_queue.put([tempworkercpu2.algo, tempworkercpu2.runs, 1, tempWaitingRRcpu2])
                self.update_result.emit([tempworkercpu2.algo, tempworkercpu2.runs, 1, tempWaitingRRcpu2])
            if tempworkercpu1.waitingSJF is not None:
                result_queue.put([tempworkercpu1.algo, tempworkercpu1.runs, 0, tempWaitingSJFcpu1])
                self.update_result.emit([tempworkercpu1.algo, tempworkercpu1.runs, 0, tempWaitingSJFcpu1])
                result_queue.put([tempworkercpu2.algo, tempworkercpu2.runs, 1, tempWaitingSJFcpu2])
                self.update_result.emit([tempworkercpu2.algo, tempworkercpu2.runs, 1, tempWaitingSJFcpu2])

            if result_queue.qsize() == otherargs[1] * 2:
                print("Finished Simulation")
                self.finished.emit()

    def _load_balance(self, process_data, cpu1_speed, cpu2_speed):
        cpu1 = []
        cpu2 = []
        x = 0
        i = 0
        while i < len(process_data):
            if x < cpu1_speed:
                if x + process_data[i][2] < cpu1_speed:
                    x += process_data[i][2]
                    cpu1.append(process_data[i])
                    process_data.pop(i)
            else:
                break
            i += 1
        y = 0
        j = 0
        while j < len(process_data):
            if y < cpu2_speed:
                if y + process_data[j][2] < cpu1_speed:
                    y += process_data[j][2]
                    cpu2.append(process_data[j])
                    process_data.pop(j)
            else:
                break
            j += 1
        if cpu1_speed > cpu2_speed:
            ratio = cpu1_speed / cpu2_speed
            for k in range(len(cpu2)):
                cpu2[k][2] *= ratio
        else:
            ratio = cpu2_speed / cpu1_speed
            for m in range(len(cpu1)):
                cpu1[m][2] *= ratio

        return cpu1, cpu2, process_data

    # This function will build a queue and
    def start_thread_process(self, queue_pile_temp):
        self.isRunning = True
        self.results = []
        # Create a Queue to hold link pile and share between threads
        item_queue = queue.Queue()
        result_queue = queue.Queue()

        otherargs = []
        queue_list_size = 0
        cpus = []
        tempprocessdata = []
        # Put all the initial items into the queue
        for item in queue_pile_temp:
            if not cpus:
                cpus.append(item)
                continue
            queue_list_size = queue_list_size + 1
            item_queue.put(item)
            tempprocessdata.append(item)

        otherargs.append(cpus)
        otherargs.append(queue_list_size)

        print("Received Data from Main Thread")
        print("Number of Process Data: " + str(queue_list_size))
        print("Process Data: " + str(tempprocessdata))
        print("CPUs : 1 - " + str(cpus[0][0]) + ", " + "2 - " + str(cpus[0][1]))

        # Append the load balancer thread to the loop
        self.load_balance_process = threading.Thread(target=self._main_process, args=(item_queue, result_queue,
                                                                                      otherargs))
        # Loop through and start all processes
        self.load_balance_process.start()
        # This .join() function prevents the script from progressing further.
        # self.load_balance_process.join()

    def stop(self):
        if self.isRunning:
            self.stopRunning = True
            print("Triggered Stop function Worker Thread!")


if __name__ == "__main__":
    # Create an array of fixed length to act as queue
    # queue_pile = list(range(queue_size))

    queue_pile = [
        [0, [
            [1, 89082, 68451, 0, 68451],
            [2, 14574, 7223, 0, 7223],
            [3, 4165, 52588, 0, 52588]
        ], 2],
        [1, [
            [1, 89082, 68451, 0],
            [2, 14574, 7223, 0],
            [3, 4165, 52588, 0]
        ], 0],
        [0, [
            [1, 63364, 24228, 0, 24228],
            [2, 77007, 54369, 0, 54369],
            [3, 72179, 9814, 0, 9814]
        ], 2],
        [1, [
            [1, 63364, 24228, 0],
            [2, 77007, 54369, 0],
            [3, 72179, 9814, 0]
        ], 0],
    ]

    # Set main process start time
    start_time = time.time()
    # Start the main process
    load = LoadBalancer()
    load.start_thread_process(queue_pile)
    result = []
    print(f"Test results on main: {load.results}")
    print(
        '[Finished processing the entire queue! Time consuming:{0} Time Finished: {1}]'.format(time.time() - start_time,
                                                                                               time.strftime("%c")))
    print(f"Results on main {result}")
