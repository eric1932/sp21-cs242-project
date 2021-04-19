"""
Typedefs.
"""
from datetime import datetime
from typing import TypedDict, NamedTuple


class TaskID(NamedTuple):
    """
    scheduler id components
    """
    username: str
    template: str
    num: str


class Task(TypedDict):
    """
    Dict that is stored under user/tasks
    """
    template: str
    period: int
    note: str
    last_success_time: datetime
    created_at: datetime
    apscheduler_id: TaskID
