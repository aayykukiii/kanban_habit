from pydantic import BaseModel, ConfigDict
from datetime import datetime


class WorkSpaceBase(BaseModel):
    name: str
    description: str | None = None
    owner_id: int


class WorkSpaceCreate(WorkSpaceBase):
    pass


class WorkSpaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    owner_id: int | None = None
    is_archived: bool | None = None


class WorkSpaceRead(WorkSpaceBase):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)