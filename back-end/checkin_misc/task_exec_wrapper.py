import importlib
from types import ModuleType
from typing import Union

from util.types import TaskID


def execute(task_id: TaskID, cookies: Union[dict, str, None]):  # pragma: no cover
    """
    Executing wrapper of checkin_tasks
    :param task_id: TaskID
    :param cookies: cookies as dictionary
    """
    task: ModuleType = importlib.import_module(f"checkin_tasks.{task_id.template}")
    try:
        task.Workflow(cookies=cookies).exec()
    except Exception as e:
        raise RuntimeError("Job Execution Failed") from e
