from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ColumnCreate(BaseModel):
    title: str
    position: int
    limit_tasks: int



class ColumnRead(BaseModel):
    id: int
    title: str
    position: int
    limit_tasks: int
    created_at: datetime


class ColumnUpdate(BaseModel):
    title: str
    position: int
    limit_tasks: int