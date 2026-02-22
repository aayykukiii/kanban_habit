from sqlalchemy import (Column, Integer, String,
                         Boolean, DateTime, Enum, ForeignKey)
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
import enum

class Base(DeclarativeBase):
    pass


class MemberRole(enum.Enum):
    member = 'member'
    viewer = 'viewer'
    admin = 'admin'


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    role = Column(Enum(MemberRole), default=MemberRole.member, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, insert_default=False)
    created_at = Column(DateTime, default=datetime.utcnow)