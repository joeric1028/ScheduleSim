from source.Library.Algorithms.NonRealTime.RoundRobin import *
from source.Library.Algorithms.NonRealTime.ShortestJobFirst import *
import logging
import threading
from concurrent import futures


class ThreadWorker:
    def __init__(self, process, mode=False, processmode=False):
        self.algo = process[0]
        self.processdata = process[1]
        self.quantum = process[2]
        self.name = process[3]
        self.mode = mode
        self.waitingRR = 0
        self.waitingSJF = 0
        self.worker = 0
        self.results = 0

        if not self.mode:
            self.run()
        else:
            self.runonthread(processmode)

    def run(self):
        print(f"Started Executing on thread {threading.get_ident()}")
        logging.info(f"Started Executing on thread {threading.get_ident()}")
        if self.algo == 0:
            print(f"Running RR on thread {threading.get_ident()}")
            logging.info(f"Running RR on thread {threading.get_ident()}")
            RR = RoundRobin()
            RR.createprocess(self.processdata, self.quantum)
            self.waitingRR = RR.getavgwaittime()
            print(f"Finished running RR on thread {threading.get_ident()}")
            logging.info(f"Finished running RR on thread {threading.get_ident()}")
        elif self.algo == 1:
            print(f"Running SJF  on thread {threading.get_ident()}")
            logging.info(f"Running SJF  on thread {threading.get_ident()}")
            SJF = ShortestJobFirst()
            SJF.createprocess(self.processdata)
            self.waitingSJF = SJF.getavgwaittime()
            print(f"Finished running SJF on thread {threading.get_ident()}")
            logging.info(f"Finished running SJF on thread {threading.get_ident()}")
        else:
            print(f"Not Executed on thread {threading.get_ident()}")
            logging.info(f"Not Executed on thread {threading.get_ident()}")

    def runonthread(self, processmode=False):  # TODO: Need running on child thread/process
        if not processmode:
            with futures.ThreadPoolExecutor as executer:
                self.results = executer.map(self.run())

    def __del__(self):
        logging.info(f"Thread {threading.get_ident()} deleted.")
