from source.Library.Algorithms.NonRealTime.RoundRobin import *
from source.Library.Algorithms.NonRealTime.ShortestJobFirst import *


class ThreadWorker:
    def __init__(self, process, mode=False):
        self.algo = process[0]
        self.processdata = process[1]
        self.quantum = process[2]
        self.mode = mode
        self.waitingRR = 0
        self.waitingSJF = 0
        self.worker = 0
        self.results = 0

        if not self.mode:
            self.run()

    def run(self):
        if self.algo == 0:
            RR = RoundRobin()
            RR.createprocess(self.processdata, self.quantum)
            self.waitingRR = RR.getavgwaittime()
        elif self.algo == 1:
            SJF = ShortestJobFirst()
            SJF.createprocess(self.processdata)
            self.waitingSJF = SJF.getavgwaittime()
