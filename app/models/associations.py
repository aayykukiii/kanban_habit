from sqlalchemy import Column, BigInteger, Table, ForeignKey
from .base import Base


task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', BigInteger, ForeignKey('task.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', BigInteger, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)