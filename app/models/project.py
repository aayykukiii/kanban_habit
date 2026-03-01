from sqlalchemy import (Column, Integer, String,
                        Boolean, DateTime, Enum,
                        ForeignKey, BigInteger)
from datetime import datetime
from sqlalchemy.orm import relationship
from .base import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    description = Column(String)
    workspace_id = Column(BigInteger, ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    boards = relationship("Board", back_populates="project", cascade="all, delete")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)