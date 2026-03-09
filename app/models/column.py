from sqlalchemy import (Column, Integer, String,
                         Boolean, DateTime, ForeignKey, BigInteger)
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.base import Base


class ColumnBase(Base):
    __tablename__ = 'columns'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    position = Column(Integer, nullable=False)
    board_id = Column(BigInteger, ForeignKey('boards.id', ondelete='CASCADE'), nullable=False)
    board = relationship('Board', back_populates='columns')
    tasks = relationship('Task', back_populates='column', cascade='all, delete')
    limit_tasks = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)