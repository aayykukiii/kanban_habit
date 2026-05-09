from sqlalchemy import Integer, String, DateTime, ForeignKey, BigInteger
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String)
    workspace_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    boards: Mapped[list['Board']] = relationship('Board', back_populates='project', cascade='all, delete')