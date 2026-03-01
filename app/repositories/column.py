from sqlalchemy.orm import Session
from schemas.column import ColumnCreate, ColumnRead, ColumnUpdate
from models.column import ColumnBase
from fastapi import HTTPException, status



def create_column(column: ColumnCreate, db: Session):
    new_column = ColumnBase(
        title=column.title,
        position=column.position,
        board_id=column.board_id,
        limit_tasks=column.limit_tasks
    )
    db.add(new_column)
    db.commit()
    db.refresh(new_column)
    return new_column


def get_all_column(db: Session):
    return db.query(ColumnBase).all()


def get_column_by_id(db: Session, column_id: int):
    return db.query(ColumnBase).filter(ColumnBase.id == column_id).first()