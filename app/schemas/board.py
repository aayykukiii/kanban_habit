from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class BoardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int


class BoardRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    project_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_archived: Optional[bool] = None