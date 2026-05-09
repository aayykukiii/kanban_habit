from sqlalchemy import Integer, String, DateTime, ForeignKey, BigInteger
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ColumnBase(Base):
    __tablename__ = 'columns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    board_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('boards.id', ondelete='CASCADE'), nullable=False)
    limit_tasks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    board: Mapped['Board'] = relationship('Board', back_populates='columns')
    tasks: Mapped[list['Task']] = relationship('Task', back_populates='column', cascade='all, delete')