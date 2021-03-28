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
    def _main_process(self, item_queue, result_queue, size):
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

            if result_queue.qsize() == size:
                print("Finished Simulation")
                self.finished.emit()

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
        self.load_balance_process = threading.Thread(target=self._main_process, args=(item_queue, result_queue,
                                                                                      queue_list_size))
        # Loop through and start all processes
        self.load_balance_process.start()
        # This .join() function prevents the script from progressing further.
        # self.load_balance_process.join()

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
