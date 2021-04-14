import importlib
from types import ModuleType

from checkin_misc.task_id import TaskID
from util.my_mongo import MyMongoInstance


def execute(task_id: TaskID, mongo: MyMongoInstance):
    """
    Executing wrapper of checkin_tasks
    :param task_id: TaskID
    :param mongo: MyMongoInstance
    """
    print("wrapper:", str(task_id))
    task: ModuleType = importlib.import_module(f"checkin_tasks.{task_id.template}")
    try:
        task.WorkFlow().exec()
        # update last_success_time
        mongo.task_update_last_success_time(task_id)
    except:
        pass
