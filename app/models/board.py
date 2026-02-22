from sqlalchemy import (Column, Integer, String,
                         Boolean, DateTime, Enum, ForeignKey)
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Board(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    description = Column(String)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    