import schedule
import time
import asyncio
import threading

import redis



redis_client = redis.Redis()



class AlertScheduler():
    """
    Use change_daily to set message sent daily
    Use change_<day of week> to set message to specific day
    All schedules pull from self.time_of_day which can be changed
    using change_time_of_day_global.  24-hour time format strings 
    e.g. "14:30"

    """

    def __init__(self, current):
        self.current = str(redis_client.get('CURRENT_SCHEDULE').decode('utf-8'))
        self.time_of_day = str(redis_client.get('TIME_OF_DAY').decode('utf-8'))
        self._schedstop = threading.Event()
        self._schedthread = threading.Thread(target=self._timer)
        self.start_scheduler()


    def _timer(self):
        while not self._schedstop.is_set():
            schedule.run_pending()
            time.sleep(3)

    def _job(self):
        print('TEST_YES')

    def start_scheduler(self):
        self._schedthread.start()
        redis_client.set('IS_SCHEDULER_RUNNING', 'True')

    def stop_job(self):
        schedule.cancel_job(self._job)
        redis_client.set('IS_SCHEDULER_RUNNING', 'False')

    def change_daily(self):
        schedule.every().day.at(f'{self.time_of_day}').do(job)


    def change_time_of_day_global(self, time_of_day):
        redis_client.set('TIME_OF_DAY', time_of_day)


    def change_second(self):
        schedule.every(4).seconds.do(self._job)

    def change_monday(self):
        schedule.every().monday.at(f'{self.time_of_day}').do(job)
        redis_client.set('CURRENT_SCHEDULE', 'MONDAY')

    def change_tuesday(self):
        schedule.every().tuesday.at(f'{self.time_of_day}').do(job)
        redis_client.set('CURRENT_SCHEDULE', 'TUESDAY')


    def change_wednesday(self):
        schedule.every().wednesday.at(f'{self.time_of_day}').do(job)
        redis_client.set('CURRENT_SCHEDULE', 'WEDNESDAY')

    def change_thursday(self):
        schedule.every().thursday.at(f'{self.time_of_day}').do(job)
        redis_client.set('CURRENT_SCHEDULE', 'THURSDAY')

    def change_friday(self):
        schedule.every().friday.at(f'{self.time_of_day}').do(job)
        redis_client.set('CURRENT_SCHEDULE', 'FRIDAY')

    def change_saturday(self):
        schedule.every().saturday.at(f'{self.time_of_day}').do(job)
        redis_client.set('CURRENT_SCHEDULE', 'SATURDAY')

    def change_sunday(self):
        schedule.every().sunday.at(f'{self.time_of_day}').do(job)
        redis_client.set('CURRENT_SCHEDULE', 'SUNDAY')

    def __repr__(self):
        return f'{self.current} at {self.time_of_day}' 
