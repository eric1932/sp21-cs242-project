from datetime import datetime
from typing import TypedDict, NamedTuple


class TaskID(NamedTuple):
    username: str
    template: str
    num: str


class Task(TypedDict):
    template: str
    period: int
    note: str
    last_success_time: datetime
    created_at: datetime
    apscheduler_id: TaskID
