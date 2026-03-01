from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ProjectCreate(BaseModel):
    title: str
    description: str
    workspace_id: int


class ProjectRead(BaseModel):
    id: int
    title: str
    description: str
    workspace_id: int
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdated(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None