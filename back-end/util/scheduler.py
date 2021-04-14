import datetime
import os
import signal
import sys
import time

import dotenv
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from util.my_mongo import MyMongoInstance

dotenv.load_dotenv()
SCHEDULER = None


def sigint_handler(sig, frame):
    if SCHEDULER:
        # SCHEDULER.pause()
        SCHEDULER.shutdown(wait=True)
        print("SIGINT shutdown")
    sys.exit(0)


def func():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func  time :', ts)


def func2():
    # 耗时2S
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func2 time：', ts)
    time.sleep(2)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)

    job_stores = {
        'default': MongoDBJobStore(database=os.getenv("DB_NAME"), collection="checkinJob",
                                   client=MyMongoInstance().client),
        'memory': MemoryJobStore()
    }
    job_defaults = {
        # 'coalesce': False,
        'max_instances': 1
    }
    SCHEDULER = BackgroundScheduler(jobstores=job_stores, job_defaults=job_defaults)
    print(MongoDBJobStore(database=os.getenv("DB_NAME"), collection="checkinJob",
                          client=MyMongoInstance().client).get_all_jobs())
    SCHEDULER.start()
    # SCHEDULER.resume()
    print(SCHEDULER.get_jobs())
    time.sleep(30)
    exit(0)

    SCHEDULER.add_job(func, trigger='interval',
                      seconds=2,
                      next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
                      id='test_job1')
    SCHEDULER.add_job(func2, trigger='interval',
                      seconds=3,
                      next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
                      id='test_job2')
    SCHEDULER.start()  # non-blocking

    while True:
        time.sleep(5)
