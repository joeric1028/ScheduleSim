# CLASS IMPLEMENTATION OF THE SHORTEST JOB FIRST SCHEDULING ALGORITHM (NON-PREEMPTIVE)
# FOR THE ALGORITHM SIMULATOR PROJECT
# DEVELOPED BY: ELIZABELLE SERDIÑA
# SUPERVISED BY: GEORGE CHARALAMBOUS
# (C)2020
import time


class ShortestJobFirst:
    def __init__(self):
        self.averageWaitingTime = 0
        self.averageTurnAroundTime = 0
        self.__start = 0
        self.__completedProcessData = []

    def createprocess(self, processdata):  # this function will create and gather the data of each of the processes
        self.__start = time.time()
        self.__executeprocess(processdata)

    def __executeprocess(self, processdata):  # this will execute the shortest job first algorithm
        startTime = []
        exitTime = []
        sTime = 0
        processdata.sort(key=lambda x: x[1])  # this will sort the processes by their arrival time

        for i in range(len(processdata)):
            readyQueue = []
            temp = []
            normalQueue = []

            for j in range(len(processdata)):
                if (processdata[j][1] <= sTime) and (processdata[j][3] == 0):
                    temp.extend([processdata[j][0], processdata[j][1], processdata[j][2]])
                    readyQueue.append(temp)
                    temp = []
                elif processdata[j][3] == 0:
                    temp.extend([processdata[j][0], processdata[j][1], processdata[j][2]])
                    normalQueue.append(temp)
                    temp = []

            if len(readyQueue) != 0:
                readyQueue.sort(key=lambda x: x[2])  # this will sort the processes by their burst time

                startTime.append(sTime)
                sTime = sTime + readyQueue[0][2]
                eTime = sTime
                exitTime.append(eTime)
                kj = 0
                for k in range(len(processdata)):
                    kj = k
                    if processdata[k][0] == readyQueue[0][0]:
                        break
                processdata[kj][3] = 1
                processdata[kj].append(eTime)

            elif len(readyQueue) == 0:
                if sTime < normalQueue[0][1]:
                    sTime = normalQueue[0][1]
                startTime.append(sTime)
                sTime = sTime + normalQueue[0][2]
                eTime = sTime
                exitTime.append(eTime)
                kj = 0
                for k in range(len(processdata)):
                    kj = k
                    if processdata[k][0] == normalQueue[0][0]:
                        break
                processdata[kj][3] = 1
                processdata[kj].append(eTime)

        self.__calculateturnaroundtime(processdata)
        self.__calculatewaitingtime(processdata)
        self.printdata(processdata)

    def __calculateturnaroundtime(self, processdata):
        totalTurnAroundTime = 0
        for i in range(len(processdata)):
            if len(processdata[i]) < 4:  # TODO: Could not calculate unfinished process Data. partial Fixed.
                turnAroundTime = 0
            else:
                turnAroundTime = processdata[i][4] - processdata[i][1]

            # turnAroundTime = completionTime - arrivalTime

            totalTurnAroundTime = totalTurnAroundTime + turnAroundTime
            processdata[i].append(turnAroundTime)
        if len(processdata) == 0:
            self.averageTurnAroundTime = 0
            return
        self.averageTurnAroundTime = totalTurnAroundTime / len(processdata)
        # averageTurnAroundTime = totalTurnAroundTime / numOfProcesses

    def __calculatewaitingtime(self, processdata):
        totalWaitingTime = 0
        for i in range(len(processdata)):
            if len(processdata[i]) < 6:  # TODO: Same problem occured and partially fixed.
                waitingTime = 0
            else:
                waitingTime = processdata[i][5] - processdata[i][2]

            # waitingTime = turnAroundTime - burstTime

            totalWaitingTime = totalWaitingTime + waitingTime
            processdata[i].append(waitingTime)
        if len(processdata) == 0:
            self.averageWaitingTime = 0
            return
        self.averageWaitingTime = totalWaitingTime / len(processdata)
        # averageWaitingTime = totalWaitingTime / noOfProcesses

    def printdata(self, processdata):
        processdata.sort(key=lambda x: x[0])  # this will sort the processes by their IDs

        print("Shortest Job First Algorithm Simulation Result\n\n"
              "processID  arrivalTime  burstTime      Completed  Completion_Time  turnAroundTime  WaitTime")

        for i in range(len(processdata)):
            for j in range(len(processdata[i])):
                print(processdata[i][j], end="				")
            print()

        print(f'Average Turnaround Time: {self.averageTurnAroundTime}')
        print(f'Average Waiting Time: {self.averageWaitingTime}')
        end = time.time()
        self.__completedProcessData = processdata
        print(f"Shortest-Job-First Execution Time = {end - self.__start} seconds\n\n")

    def getavgwaittime(self):
        return self.averageWaitingTime

    def getavgturnaroundtime(self):
        return self.averageTurnAroundTime

    def getcompletedprocessdata(self):
        return self.__completedProcessData
