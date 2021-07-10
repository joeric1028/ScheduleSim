# CLASS IMPLEMENTATION OF THE SHORTEST JOB FIRST SCHEDULING ALGORITHM (NON-PREEMPTIVE)
# FOR THE ALGORITHM SIMULATOR PROJECT
# DEVELOPED BY: ELIZABELLE SERDIÑA
# SUPERVISED BY: GEORGE CHARALAMBOUS
# (C)2020
import time


class ShortestJobFirst:
    def __init__(self):
        self.__averageWaitingTime = 0.00
        self.__totalWaitingTime = 0
        self.__averageTurnAroundTime = 0.00
        self.__totalTurnAroundTime = 0
        self.__start = 0
        self.__completedProcessData = []

    def createprocess(self, processdata):  # this function will create and gather the data of each of the processes
        self.__start = time.time()
        self.executeprocess(processdata)
        self.calculateturnaroundtime(self.__completedProcessData)
        self.calculatewaitingtime(self.__completedProcessData)
        self.printdata(self.__completedProcessData)

    def createprocess_calculate_waiting_time(self, processdata):
        self.__start = time.time()
        self.calculatewaitingtime(processdata)
        self.calculateturnaroundtime(processdata)

    def executeprocess(self, processdata):  # this will execute the shortest job first algorithm
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

        self.__completedProcessData = processdata

    def calculateturnaroundtime(self, processdata):
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
            self.__averageTurnAroundTime = 0.00
            self.__totalTurnAroundTime = 0
            return
        self.__averageTurnAroundTime = totalTurnAroundTime / len(processdata)
        # averageTurnAroundTime = totalTurnAroundTime / numOfProcesses
        self.__totalTurnAroundTime = totalTurnAroundTime

    def calculatewaitingtime(self, processdata):
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
            self.__averageWaitingTime = 0.00
            self.__totalWaitingTime = 0
            return
        self.__averageWaitingTime = totalWaitingTime / len(processdata)
        # averageWaitingTime = totalWaitingTime / noOfProcesses
        self.__totalWaitingTime = totalWaitingTime

    def printdata(self, processdata):
        processdata.sort(key=lambda x: x[0])  # this will sort the processes by their IDs

        print("Shortest Job First Algorithm Simulation Results\n\n"
              "Process ID   "
              "Arrival Time        "
              "Burst Time         "
              "Completed      "
              "Completion Time     "
              "Turnaround Time        "
              "Waiting Time")

        for i in range(len(processdata)):
            for j in range(len(processdata[i])):
                print(processdata[i][j], end="				")
            print()

        print(f'Average Turnaround Time: {self.__averageTurnAroundTime}')
        print(f'Average Waiting Time: {self.__averageWaitingTime}')
        end = time.time()
        self.__completedProcessData = processdata
        print(f"Shortest-Job-First Execution Time = {end - self.__start} seconds\n\n")

    def getavgwaittime(self):
        return self.__averageWaitingTime

    def gettotalwaittime(self):
        return self.__totalWaitingTime

    def getavgturnaroundtime(self):
        return self.__averageTurnAroundTime

    def gettotalturnaroundtime(self):
        return self.__totalTurnAroundTime

    def getcompletedprocessdata(self):
        return self.__completedProcessData
