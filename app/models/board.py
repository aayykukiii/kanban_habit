from sqlalchemy import (Column, Integer, String,
                        Boolean, DateTime, Enum,
                        ForeignKey, BigInteger)
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.base import Base


class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    description = Column(String)
    project_id = Column(BigInteger, ForeignKey('projects.id', ondelete='CASCADE'), nullable=True)
    project = relationship('Project', back_populates='boards')
    columns = relationship('ColumnBase', back_populates='board', cascade='all, delete')
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    