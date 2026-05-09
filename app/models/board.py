from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, BigInteger
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Board(Base):
    __tablename__ = 'boards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id', ondelete='CASCADE'), nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    project: Mapped['Project'] = relationship('Project', back_populates='boards')
    columns: Mapped[list['ColumnBase']] = relationship('ColumnBase', back_populates='board', cascade='all, delete')