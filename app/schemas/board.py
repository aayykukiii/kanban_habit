from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BoardBase(BaseModel):
    title: str
    description: str | None = None
    project_id: int


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_archived: bool | None = None


class BoardRead(BoardBase):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)