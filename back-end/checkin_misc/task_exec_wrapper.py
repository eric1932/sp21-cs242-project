import importlib
from types import ModuleType

from util.types import TaskID


def execute(task_id: TaskID):
    """
    Executing wrapper of checkin_tasks
    :param task_id: TaskID
    :param mongo: MyMongoInstance
    """
    print("wrapper:", str(task_id))
    task: ModuleType = importlib.import_module(f"checkin_tasks.{task_id.template}")

    task.WorkFlow().exec()
