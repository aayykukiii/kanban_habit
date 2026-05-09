from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ColumnBase(BaseModel):
    title: str
    position: int
    board_id: int
    limit_tasks: int | None = None


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(BaseModel):
    title: str | None = None
    position: int | None = None
    limit_tasks: int | None = None


class ColumnRead(ColumnBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)