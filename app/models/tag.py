from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import task_tags
from app.models.base import Base


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)

    tasks: Mapped[list['Task']] = relationship('Task', secondary=task_tags, back_populates='tags')