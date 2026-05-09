from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TaskHistory(Base):
    __tablename__ = 'task_history'

    id: Mapped[int] = mapped_column(primary_key=True)

    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    from_column_id: Mapped[int] = mapped_column(ForeignKey('columns.id'))
    to_column_id: Mapped[int] = mapped_column(ForeignKey('columns.id'))
    task = relationship('Task')