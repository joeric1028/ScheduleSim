# CLASS IMPLEMENTATION OF THE ROUND ROBIN SCHEDULING ALGORITHM
# FOR THE ALGORITHM SIMULATOR PROJECT
# DEVELOPED BY: ELIZABELLE SERDIÑA
# SUPERVISED BY: GEORGE CHARALAMBOUS
# (C)2020
import time


class RoundRobin:
    def __init__(self):
        self.__averageWaitingTime = 0.00
        self.__totalWaitingTime = 0
        self.__averageTurnAroundTime = 0.00
        self.__totalTurnAroundTime = 0
        self.__totalProc = 0
        self.__waitList = []
        self.__start = 0
        self.__execProcess = 0
        self.__completedProcessData = []

    def createprocess(self, processdata, quantum):
        # this function will create and gather the data of each of the processes
        self.__start = time.time()
        self.__executeprocesses(processdata, quantum)
        self.__calculateturnaroundtime(self.__completedProcessData)
        self.__calculatewaitingtime(self.__completedProcessData)
        self.printdata(self.__completedProcessData)

    def createprocess_calculate_waiting_time(self, processdata):
        self.__start = time.time()
        self.__calculatewaitingtime(processdata)
        self.__calculateturnaroundtime(processdata)

    def __executeprocesses(self, processdata, quantum):  # this will execute the round robin algorithm
        startTime = []
        exitTime = []
        execProcess = []
        readyQueue = []
        stime = 0
        processdata.sort(key=lambda x: x[1])  # this will sort the processes by their arrival time

        while 1:
            normalQueue = []  # this is where we store all the processes that haven't arrived yet
            temp = []
            for i in range(len(processdata)):
                if processdata[i][1] <= stime and processdata[i][3] == 0:
                    present = 0
                    if len(readyQueue) != 0:
                        for k in range(len(readyQueue)):
                            if processdata[i][0] == readyQueue[k][0]:
                                present = 1

                    # the above if checks that the next process is not a part of the ready queue

                    if present == 0:
                        temp.extend([processdata[i][0], processdata[i][1], processdata[i][2], processdata[i][4]])
                        readyQueue.append(temp)
                        temp = []

                    # the above if adds a process to the ready queue only if it is not already present in it

                    if len(readyQueue) != 0 and len(execProcess) != 0:
                        for k in range(len(readyQueue)):
                            if readyQueue[k][0] == execProcess[len(execProcess) - 1]:
                                readyQueue.insert((len(readyQueue) - 1), readyQueue.pop(k))

                    # the above if makes sure that the recently executed process is appended at the end of the ready
                    # queue

                elif processdata[i][3] == 0:
                    temp.extend([processdata[i][0], processdata[i][1], processdata[i][2], processdata[i][4]])
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
                    jk = 0
                    for j in range(len(processdata)):
                        if processdata[j][0] == readyQueue[0][0]:
                            jk = j
                            break
                    processdata[jk][2] = processdata[jk][2] - quantum
                    readyQueue.pop(0)
                elif readyQueue[0][2] <= quantum:
                    # If a process has a remaining burst time less than or equal to time quantum,
                    # it will complete its execution
                    startTime.append(stime)
                    stime = stime + readyQueue[0][2]
                    etime = stime
                    exitTime.append(etime)
                    execProcess.append(readyQueue[0][0])
                    jk = 0
                    for j in range(len(processdata)):
                        if processdata[j][0] == readyQueue[0][0]:
                            jk = j
                            break
                    processdata[jk][2] = 0
                    processdata[jk][3] = 1
                    processdata[jk].append(etime)
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
                    jk = 0
                    for j in range(len(processdata)):
                        if processdata[j][0] == normalQueue[0][0]:
                            jk = j
                            break
                    processdata[jk][2] = processdata[jk][2] - quantum
                elif normalQueue[0][2] <= quantum:
                    # If a process has a remaining burst time less than or equal to time quantum,
                    # it will complete its execution
                    startTime.append(stime)
                    stime = stime + normalQueue[0][2]
                    etime = stime
                    exitTime.append(etime)
                    execProcess.append(normalQueue[0][0])
                    jk = 0
                    for j in range(len(processdata)):
                        if processdata[j][0] == normalQueue[0][0]:
                            jk = j
                            break
                    processdata[jk][2] = 0
                    processdata[jk][3] = 1
                    processdata[jk].append(etime)

        self.__completedProcessData = processdata

    def __calculateturnaroundtime(self, processdata):
        totalTurnAroundTime = 0
        for i in range(len(processdata)):
            turnAroundTime = processdata[i][5] - processdata[i][1]

            # turnAroundTime = completionTime - arrivalTime

            totalTurnAroundTime = totalTurnAroundTime + turnAroundTime
            processdata[i].append(turnAroundTime)
        if len(processdata) == 0:
            self.__averageTurnAroundTime = 0.00
            self.__totalTurnAroundTime = 0
            return
        self.__averageTurnAroundTime = totalTurnAroundTime / len(processdata)
        # avgTurnAroundTime = totalTurnAroundTime / numOfProcesses
        self.__totalTurnAroundTime = totalTurnAroundTime

    def __calculatewaitingtime(self, processdata):
        totalWaitingTime = 0
        for i in range(len(processdata)):
            waitingTime = processdata[i][6] - processdata[i][4]

            # waitingTime = turnAroundTime - burstTime

            totalWaitingTime = totalWaitingTime + waitingTime
            processdata[i].append(waitingTime)
        if len(processdata) == 0:
            self.__averageWaitingTime = 0.00
            self.__totalWaitingTime = 0
            return
        self.__averageWaitingTime = totalWaitingTime / len(processdata)
        # avgWaitingTime = totalWaitingTime / numOfProcesses
        self.__totalWaitingTime = totalWaitingTime

    def printdata(self, processdata):
        waitingTimeList = []
        processdata.sort(key=lambda y: y[0])  # this will sort the processes by their IDs
        print("Round Robin Algorithm Simulation Results\n\n"
              "Process ID   "
              "Arrival Time     "
              "Rem Burst Time    "
              "Completed    "
              "Original Burst Time     "
              "Completion Time   "
              "Turnaround Time      "
              "Waiting Time")
        for i in range(len(processdata)):
            for j in range(len(processdata[i])):
                print(processdata[i][j], end="				")
            print()

        print(f'Average Turnaround Time: {self.__averageTurnAroundTime}')
        print(f'Average Waiting Time: {self.__averageWaitingTime}')

        self.__completedProcessData = processdata

        # print(f'Sequence of Processes: {self.execProcess}')

        for x in range(len(processdata)):
            waitingTimeList = []
            processList = []
            waitingTimeList.append(processdata[x][7])
            processList.append(processdata[x][0])
        self.__waitList = waitingTimeList
        end = time.time()
        print(f"Round-Robin Execution Time = {end - self.__start} seconds\n\n")

    def getavgwaittime(self):
        return self.__averageWaitingTime

    def gettotalwaitime(self):
        return self.__totalWaitingTime

    def getavgturnaroundtime(self):
        return self.__averageTurnAroundTime

    def gettotalturnaroundtime(self):
        return self.__totalTurnAroundTime

    def getcompletedprocessdata(self):
        return self.__completedProcessData
