from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum
from typing import Optional


class PriorityTask(StrEnum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    critical = 'critical'


class StatusType(StrEnum):
    task = 'task'
    bug = 'bug'
    feature = 'feature'


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityTask = PriorityTask.medium
    status_type: StatusType = StatusType.task
    position: int
    column_id: int
    assignee_id: Optional[int] = None
    tag_ids: Optional[list[int]] = None
    start_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    estimated_time: Optional[int] = None
    actual_time: Optional[int] = None
    is_blocked: bool = False
    blocked_reason: Optional[str] = None



class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: PriorityTask
    status_type: StatusType
    position: int
    column_id: int
    assignee_id: Optional[int]
    tag_ids: list[int]
    start_date: Optional[datetime]
    deadline: Optional[datetime]
    estimated_time: Optional[int]
    actual_time: Optional[int]
    is_blocked: bool
    blocked_reason: Optional[str]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityTask] = None
    status_type: Optional[StatusType] = None
    position: Optional[int] = None
    column_id: Optional[int] = None
    assignee_id: Optional[int] = None
    tag_ids: Optional[list[int]] = None
    start_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    estimated_time: Optional[int] = None
    actual_time: Optional[int] = None
    is_blocked: Optional[bool] = None
    blocked_reason: Optional[str] = None