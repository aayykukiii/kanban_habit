from pydantic import BaseModel, ConfigDict
import enum
from typing import Optional
from datetime import datetime


class MemberRole(enum.Enum):
    member = 'member'
    viewer = 'viewer'
    admin = 'admin'


class MemberCreate(BaseModel):
    full_name: str
    email: str
    role: MemberRole = MemberRole.member


class MemberRead(BaseModel):
    id: int
    full_name: str
    email: str
    role: MemberRole
    created_at: datetime 
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class MemberUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[MemberRole] = None