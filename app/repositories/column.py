from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.column import ColumnCreate, ColumnUpdate
from app.models.column import ColumnBase
from fastapi import HTTPException, status


async def create_column(db: AsyncSession, column: ColumnCreate):
    new_column = ColumnBase(
        title=column.title,
        position=column.position,
        board_id=column.board_id,
        limit_tasks=column.limit_tasks
    )
    db.add(new_column)
    await db.commit()
    await db.refresh(new_column)
    return new_column


async def get_all_column(db: AsyncSession):
    result = await db.execute(select(ColumnBase))
    return result.scalars().all()


async def get_column_by_id(db: AsyncSession, column_id: int):
    result = await db.execute(select(ColumnBase).where(ColumnBase.id == column_id))
    return result.scalar_one_or_none()


async def update_column_by_id(db: AsyncSession, column_id: int, column_data: ColumnUpdate):
    result = await db.execute(select(ColumnBase).where(ColumnBase.id == column_id))
    db_column = result.scalar_one_or_none()
    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='column not found')
    update_data = column_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_column, key, value)
    await db.commit()
    await db.refresh(db_column)
    return db_column


async def delete_column_by_id(db: AsyncSession, column_id: int):
    result = await db.execute(select(ColumnBase).where(ColumnBase.id == column_id))
    db_column = result.scalar_one_or_none()
    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='column not found')
    await db.delete(db_column)
    await db.commit()
    return {'detail': 'column deleted'}