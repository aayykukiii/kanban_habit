from pydantic import BaseModel, ConfigDict
from enum import Enum


class MemberRole(str, Enum):
    member = 'member'
    viewer = 'viewer'
    admin = 'admin'


class MemberBase(BaseModel):
    full_name: str
    email: str
    role: MemberRole = MemberRole.member


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None


class MemberRead(MemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)