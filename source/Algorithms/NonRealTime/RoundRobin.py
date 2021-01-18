# CLASS IMPLEMENTATION OF THE ROUND ROBIN SCHEDULING ALGORITHM
# FOR THE ALGORITHM SIMULATOR PROJECT
# DEVELOPED BY: ELIZABELLE SERDIÑA
# SUPERVISED BY: GEORGE CHARALAMBOUS
# (C)2020

import matplotlib.pyplot as plt
import random
import time


class RoundRobin:
    averageWaitingTime = 0
    totalProc = 0
    waitList = []
    start = 0

    def createProcess(self, processData,
                      quantum):  # this function will create and gather the data of each of the processes
        # quantum = int(input("Please Enter Time Quantum: "))
        global start
        start = time.time()
        RoundRobin.executeProcesses(self, processData, quantum)

    def executeProcesses(self, processData, quantum):  # this will execute the round robin algorithm
        startTime = []
        exitTime = []
        execProcess = []
        readyQueue = []
        stime = 0
        processData.sort(key=lambda x: x[1])  # this will sort the processes by their arrival time

        while 1:
            normalQueue = []  # this is where we store all the processes that haven't arrived yet
            temp = []
            for i in range(len(processData)):
                if processData[i][1] <= stime and processData[i][3] == 0:
                    present = 0
                    if len(readyQueue) != 0:
                        for k in range(len(readyQueue)):
                            if processData[i][0] == readyQueue[k][0]:
                                present = 1

                    # the above if checks that the next process is not a part of the ready queue

                    if present == 0:
                        temp.extend([processData[i][0], processData[i][1], processData[i][2], processData[i][4]])
                        readyQueue.append(temp)
                        temp = []

                    # the above if adds a process to the ready queue only if it is not already present in it

                    if len(readyQueue) != 0 and len(execProcess) != 0:
                        for k in range(len(readyQueue)):
                            if readyQueue[k][0] == execProcess[len(execProcess) - 1]:
                                readyQueue.insert((len(readyQueue) - 1), readyQueue.pop(k))

                    # the above if makes sure that the recently executed process is appended at the end of the ready queue

                elif processData[i][3] == 0:
                    temp.extend([processData[i][0], processData[i][1], processData[i][2], processData[i][4]])
                    normalQueue.append(temp)
                    temp = []
            if len(readyQueue) == 0 and len(normalQueue) == 0:
                break
            if len(readyQueue) != 0:
                if readyQueue[0][2] > quantum:
                    # If process has remaining burst time greater than the time quantum,
                    # it will execute for a time period equal to time quantum and then switch
                    startTime.append(stime)
                    stime = stime + quantum
                    etime = stime
                    exitTime.append(etime)
                    execProcess.append(readyQueue[0][0])
                    for j in range(len(processData)):
                        if processData[j][0] == readyQueue[0][0]:
                            break
                    processData[j][2] = processData[j][2] - quantum
                    readyQueue.pop(0)
                elif readyQueue[0][2] <= quantum:
                    # If a process has a remaining burst time less than or equal to time quantum,
                    # it will complete its execution
                    startTime.append(stime)
                    stime = stime + readyQueue[0][2]
                    etime = stime
                    exitTime.append(etime)
                    execProcess.append(readyQueue[0][0])
                    for j in range(len(processData)):
                        if processData[j][0] == readyQueue[0][0]:
                            break
                    processData[j][2] = 0
                    processData[j][3] = 1
                    processData[j].append(etime)
                    readyQueue.pop(0)
            elif len(readyQueue) == 0:
                if stime < normalQueue[0][1]:
                    stime = normalQueue[0][1]
                if normalQueue[0][2] > quantum:
                    # If process has remaining burst time greater than the time quantum,
                    # it will execute for a time period equal to time quantum and then switch
                    startTime.append(stime)
                    stime = stime + quantum
                    etime = stime
                    exitTime.append(etime)
                    execProcess.append(normalQueue[0][0])
                    for j in range(len(processData)):
                        if processData[j][0] == normalQueue[0][0]:
                            break
                    processData[j][2] = processData[j][2] - quantum
                elif normalQueue[0][2] <= quantum:
                    # If a process has a remaining burst time less than or equal to time quantum,
                    # it will complete its execution
                    startTime.append(stime)
                    stime = stime + normalQueue[0][2]
                    etime = stime
                    exitTime.append(etime)
                    execProcess.append(normalQueue[0][0])
                    for j in range(len(processData)):
                        if processData[j][0] == normalQueue[0][0]:
                            break
                    processData[j][2] = 0
                    processData[j][3] = 1
                    processData[j].append(etime)

        turnAroundTime = RoundRobin.calculateTurnaroundTime(self, processData)
        waitingTime = RoundRobin.calculateWaitingTime(self, processData)
        global averageWaitingTime
        averageWaitingTime = waitingTime
        RoundRobin.printData(self, processData, turnAroundTime, waitingTime, execProcess)

    def calculateTurnaroundTime(self, processData):
        totalTurnAroundTime = 0
        for i in range(len(processData)):
            turnAroundTime = processData[i][5] - processData[i][1]

            # turnAroundTime = completionTime - arrivalTime

            totalTurnAroundTime = totalTurnAroundTime + turnAroundTime
            processData[i].append(turnAroundTime)
        avgTurnAroundTime = totalTurnAroundTime / len(processData)

        # avgTurnAroundTime = totalTurnAroundTime / numOfProcesses
        return avgTurnAroundTime

    def calculateWaitingTime(self, processData):
        totalWaitingTime = 0
        for i in range(len(processData)):
            waitingTime = processData[i][6] - processData[i][4]

            # waitingTime = turnAroundTime - burstTime

            totalWaitingTime = totalWaitingTime + waitingTime
            processData[i].append(waitingTime)
        avgWaitingTime = totalWaitingTime / len(processData)

        # avgWaitingTime = totalWaitingTime / numOfProcesses
        return avgWaitingTime

    def printData(self, processData, avgTurnAroundTime, avgWaitingTime, execProcess):
        processData.sort(key=lambda x: x[0])  # this will sort the processes by their IDs
        print(
            "Process ID  Arrival Time  Rem Burst Time   Completed  Original Burst Time  Completion Time  Turnaround Time  Waiting Time")
        for i in range(len(processData)):
            for j in range(len(processData[i])):
                print(processData[i][j], end="				")
            print()

        print(f'Average Turnaround Time: {avgTurnAroundTime}ms')

        print(f'Average Waiting Time: {avgWaitingTime}ms')

        print(f'Sequence of Processes: {execProcess}')

        for x in range(len(processData)):
            waitingTimeList = []
            processList = []
            waitingTimeList.append(processData[x][7])
            processList.append(processData[x][0])
        waitList = waitingTimeList
        end = time.time()
        print(f"Round-Robin Execution Time = {end - start}")

    def getAvgWaitTime(self):
        return averageWaitingTime

    def getNumOfProcesses(self):
        return totalProc