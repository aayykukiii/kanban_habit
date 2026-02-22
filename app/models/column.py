from sqlalchemy import (Column, Integer, String,
                         Boolean, DateTime, Enum, ForeignKey)
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Column(Base):
    __tablename__ = 'columns'

    id = Column(Integer, primary_kay=True)
    title = Column(String, nullable=True)
    position = Column(Integer)
    limit_tasks = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcfromtimestamp)