import importlib
from types import ModuleType

from util.types import TaskID


def execute(task_id: TaskID):  # pragma: no cover
    """
    Executing wrapper of checkin_tasks
    :param task_id: TaskID
    """
    task: ModuleType = importlib.import_module(f"checkin_tasks.{task_id.template}")
    task.Workflow().exec()
