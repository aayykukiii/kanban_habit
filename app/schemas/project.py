from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ProjectBase(BaseModel):
    title: str
    description: str
    workspace_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)