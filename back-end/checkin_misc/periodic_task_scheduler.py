import datetime
import os

import dotenv
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from checkin_misc import task_exec_wrapper
from util.types import TaskID
from util.my_mongo import MyMongoInstance

# set up scheduler
dotenv.load_dotenv()
_job_stores = {
    'default': MongoDBJobStore(database=os.getenv("DB_NAME"), collection="checkinJob",
                               client=MyMongoInstance().client),
    'memory': MemoryJobStore()
}
_job_defaults = {
    # 'coalesce': False,
    'max_instances': 1
}
_executors = {
    'default': ThreadPoolExecutor()
}
SCHEDULER = BackgroundScheduler(jobstores=_job_stores, job_defaults=_job_defaults, executors=_executors)


def api_startup():
    print(MongoDBJobStore(database=os.getenv("DB_NAME"), collection="checkinJob",
                          client=MyMongoInstance().client).get_all_jobs())
    SCHEDULER.start()
    # SCHEDULER.resume()


def api_shutdown():
    SCHEDULER.shutdown(wait=True)


def find_job_available_id(username: str, template: str):
    iter_num = 0
    # compose
    while True:
        task_id = f"{username}-{template}-{iter_num}"
        if not SCHEDULER.get_job(task_id):
            break
        else:
            iter_num += 1
    return iter_num


def add_task(period: int, task_id: TaskID):
    SCHEDULER.add_job(task_exec_wrapper.execute, trigger='interval',
                      kwargs={"task_id": task_id},
                      seconds=period,
                      next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
                      id=str(task_id))
