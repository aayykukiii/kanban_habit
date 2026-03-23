from sqlalchemy import (
    Column, Integer, String,
    Boolean, DateTime, Enum,
    ForeignKey, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.models.base import Base
from app.models.associations import task_tags


class PriorityTask(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    critical = 'critical'


class StatusType(enum.Enum):
    task = 'task'
    bug = 'bug'
    feature = 'feature'


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum(PriorityTask, name='priority_task'), default=PriorityTask.medium, nullable=False)
    status_type = Column(Enum(StatusType, name='status_type'), default=StatusType.task, nullable=False)
    position = Column(Integer, nullable=False)

    column_id = Column(BigInteger, ForeignKey('columns.id', ondelete='CASCADE'), nullable=False)
    member_id = Column(BigInteger, ForeignKey('members.id'), nullable=True)
    member = relationship('Member', back_populates='tasks')
    column = relationship('ColumnBase', back_populates='tasks')
    tags = relationship(
        'Tag',
        secondary=task_tags,
        back_populates='tasks',
        lazy='joined'
    )

    start_date = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    estimated_time = Column(Integer, nullable=True)
    actual_time = Column(Integer, nullable=True)
    is_blocked = Column(Boolean, default=False, nullable=False)
    blocked_reason = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)