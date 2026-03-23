from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime


class MemberRole(str, Enum):
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

    class Config:
        from_attributes = True



class MemberUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[MemberRole] = None