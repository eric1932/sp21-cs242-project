from datetime import datetime
from typing import TypedDict

from checkin_misc.task_id import TaskID


class Task(TypedDict):
    template: str
    period: int
    note: str
    last_success_time: datetime
    created_at: datetime
    apscheduler_id: TaskID
