from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.column import (create_column, get_all_column, get_column_by_id,
                                 update_column_by_id, delete_column_by_id)
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from app.schemas.column import ColumnCreate, ColumnRead, ColumnUpdate


router = APIRouter()


@router.post('/column', response_model=ColumnRead)
async def post_column(column: ColumnCreate, db: AsyncSession = Depends(get_db)):
    return await create_column(db, column)



@router.get('/column', response_model=list[ColumnRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_column(db)


@router.get('/column/{column_id}', response_model=ColumnRead)
async def get_column(column_id: int, db: AsyncSession = Depends(get_db)):
    column = await get_column_by_id(db, column_id)
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='member not found')
    return column



@router.put('/column/{column_id}', response_model=ColumnUpdate)
async def update_column(column_id: int, column: ColumnUpdate, db: AsyncSession = Depends(get_db)):
    return await update_column_by_id(db, column_id, column)


@router.delete('/column/{column_id}')
async def delete_column(column_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_column_by_id  (db, column_id)