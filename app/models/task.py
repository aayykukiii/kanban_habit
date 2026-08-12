from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Boolean, DateTime, Enum, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base
from app.models.associations import task_tags


class PriorityTask(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class StatusType(PyEnum):
    task = "task"
    bug = "bug"
    feature = "feature"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    priority: Mapped[PriorityTask] = mapped_column(
        Enum(PriorityTask, name="priority_task"),
        default=PriorityTask.medium,
        nullable=False,
    )
    status_type: Mapped[StatusType] = mapped_column(
        Enum(StatusType, name="status_type"),
        default=StatusType.task,
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    column_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("columns.id", ondelete="CASCADE"),
        nullable=False,
    )
    member_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("members.id"),
        nullable=True,
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    author: Mapped["User"] = relationship(
        "User",
        back_populates="tasks",
    )
    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="tasks",
    )
    column: Mapped["ColumnBase"] = relationship(
        "ColumnBase",
        back_populates="tasks",
    )
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=task_tags,
        back_populates="tasks",
        lazy="joined",
    )

    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    estimated_time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    blocked_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )