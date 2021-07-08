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
        self.cpu1_speed = None
        self.cpu2_speed = None
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
            tempProcessData = []
            temp_Algo_Mode = item[0]
            temp_runs = item[1]
            process_data = item[2]
            temp_quantum = item[3]

            temp_cpu1_tat = 0
            temp_cpu1_wt = 0
            temp_cpu1_proc_total = 0
            temp_cpu2_proc_total = 0
            temp_cpu2_tat = 0
            temp_cpu2_wt = 0
            self.cpu1_speed = otherargs[0][0]
            self.cpu2_speed = otherargs[0][1]

            while len(process_data) != 0:
                if self.stopRunning:
                    return

                cpu_1, cpu_2, process_data = self._load_balance(process_data)

                if len(cpu_1) != 0:
                    temp_cpu1_proc_total += len(cpu_1)
                    tempworkercpu1 = ThreadWorker([temp_Algo_Mode, temp_runs, cpu_1, temp_quantum])
                    tempProcessData += tempworkercpu1.completedProcessData
                    temp_cpu1_tat += tempworkercpu1.turnaround
                    temp_cpu1_wt += tempworkercpu1.waiting
                if len(cpu_2) != 0:
                    temp_cpu2_proc_total += len(cpu_2)
                    tempworkercpu2 = ThreadWorker([temp_Algo_Mode, temp_runs, cpu_2, temp_quantum])
                    tempProcessData += tempworkercpu2.completedProcessData
                    temp_cpu2_tat += tempworkercpu2.turnaround
                    temp_cpu2_wt += tempworkercpu2.waiting

            if temp_cpu2_proc_total != 0:
                temp_cpu1_tat = temp_cpu1_tat / temp_cpu1_proc_total
                temp_cpu1_wt = temp_cpu1_wt / temp_cpu1_proc_total

            cpumode = 0
            if otherargs[0][2] == 0:
                cpumode = 1
                if temp_cpu2_proc_total != 0:
                    temp_cpu2_tat = temp_cpu2_tat / temp_cpu2_proc_total
                    temp_cpu2_wt = temp_cpu2_wt / temp_cpu2_proc_total

            result_queue.put([temp_Algo_Mode, cpumode, temp_runs, temp_cpu1_wt, temp_cpu1_tat,
                              temp_cpu2_wt, temp_cpu2_tat])
            self.update_result.emit([temp_Algo_Mode, cpumode, temp_runs, temp_cpu1_wt,
                                     temp_cpu1_tat, temp_cpu2_wt, temp_cpu2_tat])

            if result_queue.qsize() == otherargs[1]:
                print("Finished Simulation")
                self.finished.emit()

    def _load_balance(self, process_data):
        cpu1_bt_total = 0
        cpu2_bt_total = 0
        cpu_1 = []
        cpu_2 = []
        extra = []
        if self.cpu1_speed != 0 and self.cpu2_speed != 0:
            multiplier = self.cpu1_speed / self.cpu2_speed
        else:
            multiplier = 1

        for i in range(len(process_data)):
            if cpu1_bt_total < self.cpu1_speed:
                cpu1_bt_total += process_data[i][2]
                if self.cpu1_speed < self.cpu2_speed:
                    process_data[i][2] *= multiplier
                cpu_1.append(process_data[i])

            elif cpu2_bt_total < self.cpu2_speed:
                cpu2_bt_total += process_data[i][2]
                if self.cpu2_speed < self.cpu1_speed:
                    process_data[i][2] *= multiplier
                cpu_2.append(process_data[i])

            else:
                extra.append(process_data[i])

        return cpu_1, cpu_2, extra

    # This function will build a queue and
    def start_thread_process(self, queue_pile_temp):
        self.isRunning = True
        self.results = []
        # Create a Queue to hold link pile and share between threads
        item_queue = queue.Queue()
        result_queue = queue.Queue()

        otherargs = []
        queue_list_size = 0
        tempprocessdata = []
        # Put all the initial items into the queue
        for item in queue_pile_temp:
            if not otherargs:
                otherargs.append(item)
                continue
            queue_list_size = queue_list_size + 1
            item_queue.put(item)
            tempprocessdata.append(item)

        otherargs.append(queue_list_size)

        print("Received Data from Main Thread")
        print("Number of Process Data: " + str(queue_list_size))
        print("Process Data: " + str(tempprocessdata))
        if otherargs[0][2] == 0:
            print("CPUs : 1 - " + str(otherargs[0][0]) + ", " + "2 - " + str(otherargs[0][1]))
        elif otherargs[0][2] == 1:
            print("1 CPU only")

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
