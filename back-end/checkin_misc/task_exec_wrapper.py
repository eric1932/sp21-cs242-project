import importlib
from types import ModuleType

from util.types import TaskID
from util.my_mongo import static_get_mongo_instance


def execute(task_id: TaskID):
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
        static_get_mongo_instance().task_update_last_success_time(task_id)
    except:
        pass
