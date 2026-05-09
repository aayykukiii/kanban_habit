from sqlalchemy import Integer, String, DateTime, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models.base import Base


class MemberRole(enum.Enum):
    member = 'member'
    viewer = 'viewer'
    admin = 'admin'


class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    role: Mapped[MemberRole] = mapped_column(Enum(MemberRole), default=MemberRole.member)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tasks: Mapped[list['Task']] = relationship('Task', back_populates='member')