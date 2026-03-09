from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.board import (create_board, get_all_board, get_board_by_id,
                                update_board_by_id, deleted_board_by_id)
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from app.schemas.board import BoardCreate, BoardRead, BoardUpdate


router = APIRouter()


@router.post('/board', response_model=BoardRead)
async def post_board(board: BoardCreate, db: AsyncSession = Depends(get_db)):
    return await create_board(db, board)



@router.get('/board', response_model=list[BoardRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_board(db)


@router.get('/board/{board_id}', response_model=BoardRead)
async def get_board(board_id: int, db: AsyncSession = Depends(get_db)):
    board = await get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='member not found')
    return board



@router.put('/board/{board_id}', response_model=BoardUpdate)
async def update_board(board_id: int, board: BoardUpdate, db: AsyncSession = Depends(get_db)):
    return await update_board_by_id(db, board_id, board)


@router.delete('/board/{board_id}')
async def delete_board(board_id: int, db: AsyncSession = Depends(get_db)):
    return await deleted_board_by_id(db, board_id)