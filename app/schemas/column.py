from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ColumnCreate(BaseModel):
    title: str
    position: int
    board_id: int
    limit_tasks: Optional[int] = None


class ColumnRead(BaseModel):
    id: int
    title: str
    position: int
    board_id: int
    limit_tasks: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ColumnUpdate(BaseModel):
    title: Optional[str] = None
    position: Optional[int] = None
    limit_tasks: Optional[int] = None