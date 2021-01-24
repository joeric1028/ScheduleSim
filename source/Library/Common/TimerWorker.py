import logging
import time
from multiprocessing import Process

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %('
                           'message)s')

logger = logging.getLogger(__name__)


class TimerWorker:
    def __init__(self, starttime, mode=False):
        self.mode = mode
        self.time = starttime
        self.timeelapsed = 0
        self.timestop = 0
        self.process1 = Process(target=self.run)
        if not self.mode:
            self.run()
        else:
            self.runonprocess()

    def run(self):
        print("\n")
        logging.info("Started Timer.")
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

    def runonprocess(self):
        self.process1.start()

    def __del__(self):
        self.process1.terminate()
        logging.info("Stopped Timer.")
