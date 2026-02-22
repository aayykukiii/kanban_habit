from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum
from typing import Optional


class PriorityTask(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class StatusType(StrEnum):
    task = "task"
    bug = "bug"
    feature = "feature"



class TaskCreate(BaseModel):
    title: str
    description: str
    priority: PriorityTask = PriorityTask.medium
    status_type: StatusType = StatusType.task
    position: int
    board_id: int
    column_id: int
    assignee_id: int
    start_date: datetime
    deadline: datetime
    estimated_time: datetime
    actual_time: datetime
    is_blocked: bool
    blocked_reason: str
    completed_at: datetime


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    priority: PriorityTask
    status_type: StatusType
    position: int
    board_id: int
    column_id: int
    assignee_id: int
    start_date: datetime
    deadline: datetime
    estimated_time: datetime
    actual_time: datetime
    is_blocked: bool
    blocked_reason: str
    completed_at: datetime


    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityTask] = None
    status_type: Optional[StatusType] = None
    position: Optional[int] = None
    is_blocked: Optional[bool] = None
    blocked_reason: Optional[str] = None