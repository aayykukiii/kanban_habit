from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum


class PriorityTask(StrEnum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    critical = 'critical'


class StatusType(StrEnum):
    task = 'task'
    bug = 'bug'
    feature = 'feature'


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    priority: PriorityTask = PriorityTask.medium
    status_type: StatusType = StatusType.task
    position: int
    column_id: int
    member_id: int | None = None
    start_date: datetime | None = None
    deadline: datetime | None = None
    estimated_time: int | None = None
    actual_time: int | None = None
    is_blocked: bool = False
    blocked_reason: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: PriorityTask | None = None
    status_type: StatusType | None = None
    position: int | None = None
    column_id: int | None = None
    member_id: int | None = None
    start_date: datetime | None = None
    deadline: datetime | None = None
    estimated_time: int | None = None
    actual_time: int | None = None
    is_blocked: bool | None = None
    blocked_reason: str | None = None


class TaskRead(TaskBase):
    id: int
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)