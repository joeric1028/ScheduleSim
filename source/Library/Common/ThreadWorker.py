from source.Library.Algorithms.NonRealTime.RoundRobin import *
from source.Library.Algorithms.NonRealTime.ShortestJobFirst import *


class ThreadWorker:
    def __init__(self, process, mode=False):
        self.algo = process[0]
        self.runs = process[1]
        self.processdata = process[2]
        self.quantum = process[3]
        self.mode = mode
        self.completedProcessData = []
        self.waiting = 0.00
        self.turnaround = 0.00
        self.worker = 0
        self.results = 0

        if not self.mode:
            self.run()

    def run(self):
        if self.algo == 0:
            RR = RoundRobin()
            RR.createprocess(self.processdata, self.quantum)
            self.waiting = RR.gettotalwaitime()
            self.turnaround = RR.gettotalturnaroundtime()
            self.completedProcessData = RR.getcompletedprocessdata()
        elif self.algo == 1:
            SJF = ShortestJobFirst()
            SJF.createprocess(self.processdata)
            self.waiting = SJF.gettotalwaittime()
            self.turnaround = SJF.gettotalturnaroundtime()
            self.completedProcessData = SJF.getcompletedprocessdata()

    def calculate_waiting_time(self):
        if self.algo == 0:
            RR = RoundRobin()
            RR.createprocess_calculate_waiting_time(self.processdata)
            self.waiting = RR.gettotalwaitime()
            self.turnaround = RR.gettotalturnaroundtime()
            self.completedProcessData = RR.getcompletedprocessdata()
        elif self.algo == 1:
            SJF = ShortestJobFirst()
            SJF.createprocess_calculate_waiting_time(self.processdata)
            self.waiting = SJF.gettotalwaittime()
            self.turnaround = SJF.gettotalturnaroundtime()
            self.completedProcessData = SJF.getcompletedprocessdata()
