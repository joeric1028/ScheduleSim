import time


class TimerWorker:
    def __init__(self, starttime, mode=False):
        self.mode = mode
        self.time = starttime
        self.timeelapsed = 0
        self.timestop = 0
        if not self.mode:
            self.run()

    def run(self):
        print("\n")
        while self.timestop != 1:
            self.timeelapsed = time.time()
            timer = self.timeelapsed - self.time
            hours = time.strftime("%H", time.gmtime(timer))
            mins = time.strftime("%M", time.gmtime(timer))
            if int(hours) != 0 and int(mins) != 0:
                t = time.strftime("%H hours %M minutes %S seconds", time.gmtime(timer))
            elif int(mins) > 0:
                t = time.strftime("%M minutes %S seconds", time.gmtime(timer))
            else:
                t = time.strftime("%S seconds", time.gmtime(timer))
            print(f'\rRunning Simulation - Time Elapsed: {t}', end="")
            time.sleep(0.5)
