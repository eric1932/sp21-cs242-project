"""
Typedefs.
"""
from datetime import datetime
from enum import Enum
from typing import TypedDict, NamedTuple


class TaskID(NamedTuple):
    """
    scheduler id components
    """
    username: str
    template: str
    num: str


class TaskStatus(Enum):
    FIRST_RUN = 0
    SUCCESS = 1
    ERROR = 2


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
    status: TaskStatus
