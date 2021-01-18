# CLASS IMPLEMENTATION OF THE SHORTEST JOB FIRST SCHEDULING ALGORITHM (NON-PREEMPTIVE)
# FOR THE ALGORITHM SIMULATOR PROJECT
# DEVELOPED BY: ELIZABELLE SERDIÑA
# SUPERVISED BY: GEORGE CHARALAMBOUS
# (C)2020

import random
import time


class ShortestJobFirst:
    averageWaitingTime = 0
    totalProc = 0
    start = 0

    def createProcess(self, processData):  # this function will create and gather the data of each of the processes
        global start
        start = time.time()
        ShortestJobFirst.executeProcess(self, processData)

    def executeProcess(self, processData):  # this will execute the shortest job first algorithm
        startTime = []
        exitTime = []
        sTime = 0
        processData.sort(key=lambda x: x[1])  # this will sort the processes by their arrival time

        for i in range(len(processData)):
            readyQueue = []
            temp = []
            normalQueue = []

            for j in range(len(processData)):
                if (processData[j][1] <= sTime) and (processData[j][3] == 0):
                    temp.extend([processData[j][0], processData[j][1], processData[j][2]])
                    readyQueue.append(temp)
                    temp = []
                elif processData[j][3] == 0:
                    temp.extend([processData[j][0], processData[j][1], processData[j][2]])
                    normalQueue.append(temp)
                    temp = []

            if len(readyQueue) != 0:
                readyQueue.sort(key=lambda x: x[2])  # this will sort the processes by their burst time

                startTime.append(sTime)
                sTime = sTime + readyQueue[0][2]
                eTime = sTime
                exitTime.append(eTime)
                for k in range(len(processData)):
                    if processData[k][0] == readyQueue[0][0]:
                        break
                processData[k][3] = 1
                processData[k].append(eTime)

            elif len(readyQueue) == 0:
                if sTime < normalQueue[0][1]:
                    sTime = normalQueue[0][1]
                startTime.append(sTime)
                sTime = sTime + normalQueue[0][2]
                eTime = sTime
                exitTime.append(eTime)
                for k in range(len(processData)):
                    if processData[k][0] == normalQueue[0][0]:
                        break
                processData[k][3] = 1
                processData[k].append(eTime)

        totalTime = ShortestJobFirst.calculateTurnaroundTime(self, processData)
        waitingTime = ShortestJobFirst.calculateWaitingTime(self, processData)
        global averageWaitingTime
        averageWaitingTime = waitingTime
        ShortestJobFirst.printData(self, processData, totalTime, waitingTime)

    def calculateTurnaroundTime(self, processData):
        totalTurnAroundTime = 0
        for i in range(len(processData)):
            turnAroundTime = processData[i][4] - processData[i][1]

            # turnAroundTime = completionTime - arrivalTime

            totalTurnAroundTime = totalTurnAroundTime + turnAroundTime
            processData[i].append(turnAroundTime)
        avgTurnAroundTime = totalTurnAroundTime / len(processData)
        # averageTurnAroundTime = totalTurnAroundTime / numOfProcesses

        return avgTurnAroundTime

    def calculateWaitingTime(self, processData):
        totalWaitingTime = 0
        for i in range(len(processData)):
            waitingTime = processData[i][5] - processData[i][2]

            # waitingTime = turnAroundTime - burstTime

            totalWaitingTime = totalWaitingTime + waitingTime
            processData[i].append(waitingTime)
        avgWaitingTime = totalWaitingTime / len(processData)
        # averageWaitingTime = totalWaitingTime / noOfProcesses

        return avgWaitingTime

    def printData(self, processData, avgTurnAroundTime, avgWaitingTime):
        processData.sort(key=lambda x: x[0])  # this will sort the processes by their IDs

        print("processID  arrivalTime  burstTime      Completed  Completion_Time  turnAroundTime  WaitTime")

        for i in range(len(processData)):
            for j in range(len(processData[i])):
                print(processData[i][j], end="				")
            print()

        print(f'Average Turnaround Time: {avgTurnAroundTime}')
        print(f'Average Waiting Time: {avgWaitingTime}')
        end = time.time()
        print(f"Shortest-Job-First Execution Time = {end - start}")

    def getAvgWaitTime(self):
        return averageWaitingTime

    def getNumOfProcesses(self):
        return totalProc