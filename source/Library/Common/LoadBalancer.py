# Import Python modules
import os
import queue
import threading
import time

import psutil
from PyQt5.QtCore import *

from source.Library.Common.ThreadWorker import ThreadWorker


class LoadBalancer(QObject):
    update_result = pyqtSignal(list)
    finished = pyqtSignal()
    exited = pyqtSignal()

    def __init__(self, args, parent=None):
        super().__init__(parent)
        self.argArray = args
        self.results = []
        self.isRunning = False
        self.stopRunning = False
        self.load_balance_process = None
        parent.startSimulate.connect(self.start_thread_process)
        parent.stopSimulate.connect(self.stop)

    def __del__(self):
        del self.results
        del self.load_balance_process

    # Main task function
    def _main_process(self, item_queue, result_queue, queue_size):
        # Go through each link in the array passed in.
        while not item_queue.empty():
            if self.stopRunning:
                return

            # Get the next item in the queue
            item = item_queue.get()

            tempworker = ThreadWorker(item)

            if tempworker.waitingRR is not None:
                result_queue.put([tempworker.algo, tempworker.runs, tempworker.waitingRR])
                self.update_result.emit([tempworker.algo, tempworker.runs, tempworker.waitingRR])
            if tempworker.waitingSJF is not None:
                result_queue.put([tempworker.algo, tempworker.runs, tempworker.waitingSJF])
                self.update_result.emit([tempworker.algo, tempworker.runs, tempworker.waitingSJF])

            if result_queue.qsize() == queue_size:
                self.finished.emit()

            print(f"Show args on load balance executor: {self.argArray}")

            if self._spool_down_load_balance():
                print("Process " + str(os.getpid()) + " saying goodnight...")
                break

    # This function will build a queue and
    def start_thread_process(self, queue_pile_temp):
        self.isRunning = True
        self.results = []
        # Create a Queue to hold link pile and share between threads
        item_queue = queue.Queue()
        result_queue = queue.Queue()

        queue_list_size = 0
        # Put all the initial items into the queue
        for item in queue_pile_temp:
            queue_list_size = queue_list_size + 1
            item_queue.put(item)
        # Append the load balancer thread to the loop
        self.load_balance_process = threading.Thread(target=self._spool_up_load_balance, args=(item_queue,
                                                                                               result_queue,
                                                                                               queue_list_size))
        # Loop through and start all processes
        self.load_balance_process.start()
        # This .join() function prevents the script from progressing further.
        # self.load_balance_process.join()

        print(f" Shows Final Result under Start Thread Process: {self.results}")

    # Spool down the thread balance when load is too high
    def _spool_down_load_balance(self):
        # Get the count of CPU cores
        core_count = psutil.cpu_count()
        # Calulate the short term load average of past minute
        one_minute_load_average = psutil.getloadavg()[0] / core_count
        # If load balance above the max return True to kill the process
        if one_minute_load_average > self.argArray['cpu_target']:
            print("-Unacceptable load balance detected. Killing process " + str(os.getpid()) + "...")
            return True
        return False

    # Load balancer thread function
    def _spool_up_load_balance(self, item_queue, result_queue, queue_size):
        print("[Starting load balancer...]")
        # Get the count of CPU cores
        core_count = psutil.cpu_count()
        # While there is still links in queue
        while not item_queue.empty():
            if self.stopRunning:
                self.isRunning = False
                self.stopRunning = False
                print("Worker thread function on Spool up balance is stopped!")
                return
            print("[Calculating load balance...]")
            # Check the 1 minute average CPU load balance
            # returns 1,5,15 minute load averages
            one_minute_load_average = psutil.getloadavg()[0] / core_count
            # If the load average much less than target, start a group of new threads
            if one_minute_load_average < self.argArray['cpu_target'] / 2:
                # Print message and log that load balancer is starting another thread
                print("Starting another thread group due to low CPU load balance of: " + str(
                    one_minute_load_average * 100) + "%")
                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return
                time.sleep(5)

                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return
                # Start another group of threads
                for i in range(3):
                    start_new_thread = threading.Thread(target=self._main_process, args=(item_queue,
                                                                                         result_queue, queue_size))
                    start_new_thread.start()
                # Allow the added threads to have an impact on the CPU balance
                # before checking the one minute average again
                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return
                time.sleep(10)
                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return

            # If load average less than target start single thread
            elif one_minute_load_average < self.argArray['cpu_target']:
                # Print message and log that load balancer is starting another thread
                print("Starting another single thread due to low CPU load balance of: " + str(
                    one_minute_load_average * 100) + "%")
                # Start another thread
                start_new_thread = threading.Thread(target=self._main_process, args=(item_queue, result_queue,
                                                                                     queue_size))
                start_new_thread.start()
                # Allow the added threads to have an impact on the CPU balance
                # before checking the one minute average again
                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return
                time.sleep(10)
                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return

            else:
                # Print CPU load balance
                print("Reporting stable CPU load balance: " + str(one_minute_load_average * 100) + "%")
                # Sleep for another minute while
                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return
                time.sleep(10)
                if self.stopRunning:
                    self.isRunning = False
                    self.stopRunning = False
                    print("Worker thread function on Spool up balance is stopped!")
                    return

    def stop(self):
        if self.isRunning:
            self.stopRunning = True
            print("Triggered Stop function Worker Thread!")


if __name__ == "__main__":
    # Set the queue size
    queue_size = 10000
    # Define an arguments array to pass around all the values
    args_array = {
        # Set some initial CPU load values as a CPU usage goal
        "cpu_target": 0.60,
        # When CPU load is significantly low, start this number
        # of threads
        "thread_group_size": 3
    }

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
    load = LoadBalancer(args_array)
    load.start_thread_process(queue_pile)
    result = []
    print(f"Test results on main: {load.results}")
    print(
        '[Finished processing the entire queue! Time consuming:{0} Time Finished: {1}]'.format(time.time() - start_time,
                                                                                               time.strftime("%c")))
    print(f"Results on main {result}")
