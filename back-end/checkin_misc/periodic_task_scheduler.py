import datetime
import os
from typing import Union

import dotenv
from apscheduler.events import EVENT_JOB_EXECUTED, JobExecutionEvent, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from checkin_misc import task_exec_wrapper
from util.my_mongo import MyMongoInstance
from util.types import TaskID

mongo = MyMongoInstance()

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


def event_listener_success(event: JobExecutionEvent):  # pragma: no cover
    # update last_success_time
    mongo.task_update_last_success_time_and_set_status_to_success(event.job_id)


def event_listener_error(event: JobExecutionEvent):
    mongo.task_set_status_to_err(event.job_id)


def api_startup():  # pragma: no cover
    SCHEDULER.start()
    # SCHEDULER.resume()

    SCHEDULER.add_listener(event_listener_success, EVENT_JOB_EXECUTED)
    SCHEDULER.add_listener(event_listener_error, EVENT_JOB_ERROR)


def api_shutdown():  # pragma: no cover
    SCHEDULER.shutdown(wait=True)


def find_job_available_id(username: str, template: str):
    iter_num = 0
    # compose
    while True:
        task_id = f"{username}-{template}-{iter_num}"  # TODO uuid
        if not SCHEDULER.get_job(task_id):
            break
        else:
            iter_num += 1
    return iter_num


def add_task(period: int, task_id: TaskID, cookies: Union[dict, str, None]):
    SCHEDULER.add_job(task_exec_wrapper.execute, trigger='interval',
                      kwargs={"task_id": task_id, "cookies": cookies},
                      seconds=period,
                      next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
                      id='-'.join(task_id))
