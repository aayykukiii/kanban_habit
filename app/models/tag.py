from sqlalchemy import (Column, Integer, String,
                        Boolean, DateTime, Enum, 
                        ForeignKey, BigInteger)
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.associations import task_tags
from app.models.base import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=True)  

    tasks = relationship(
        'Task', secondary=task_tags, back_populates='tags'
    )