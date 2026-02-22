from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class WorkSpaceCreate(BaseModel):
    name: str
    decsription: str


class WorkSpaceRead(BaseModel):
    id: int
    name: str
    description: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkSpaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_archived: Optional[bool] = None