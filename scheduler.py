import schedule
import time
import logging
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.jobs = []
        self.logger = logging.getLogger("Scheduler")

    def schedule(self, worker, run_at=None, interval=None):
        if run_at:
            run_time = datetime.strptime(run_at, "%Y-%m-%d %H:%M:%S")
            if run_time < datetime.now():
                self.logger.warning(f"Scheduled time {run_at} has already passed. Worker {worker} will run immediately.")
                worker.start()
            else:
                self.logger.info(f"Scheduling worker {worker} to run at {run_at}.")
                schedule.every().day.at(run_time.strftime("%H:%M:%S")).do(worker.start)
        elif interval:
            self.logger.info(f"Scheduling worker {worker} to run every {interval} seconds.")
            schedule.every(interval).seconds.do(worker.start)
        self.jobs.append(worker)

    def start(self, interval=1):
        while True:
            schedule.run_pending()
            time.sleep(interval)
