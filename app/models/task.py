from sqlalchemy import (
    Column, Integer, String,
    Boolean, DateTime, Enum,
    ForeignKey, BigInteger,
    UniqueConstraint
)
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
import enum


class Base(DeclarativeBase):
    pass


class PriorityTask(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class StatusType(enum.Enum):
    task = "task"
    bug = "bug"
    feature = "feature"


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (UniqueConstraint("column_id", "position"))

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum(PriorityTask), default=PriorityTask.medium, nullable=False)
    status_type = Column(Enum(StatusType), default=StatusType.task, nullable=False)
    position = Column(Integer, nullable=False)

    board_id = Column(BigInteger, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    column_id = Column(BigInteger, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)
    assignee_id = Column(BigInteger, ForeignKey("members.id"), nullable=True)

    start_date = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    estimated_time = Column(Integer, nullable=True)
    actual_time = Column(Integer, nullable=True)
    is_blocked = Column(Boolean, default=False, nullable=False)
    blocked_reason = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)