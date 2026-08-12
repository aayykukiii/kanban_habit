from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_manager
from app.core.db import get_db
from app.models.users import User
from app.repositories.board import (
    create_board,
    get_all_board,
    get_board_by_id,
    update_board_by_id,
    deleted_board_by_id,
)
from app.schemas.board import BoardCreate, BoardRead, BoardUpdate


router = APIRouter()


@router.post("/", response_model=BoardRead)
async def post_board(board: BoardCreate, db: AsyncSession = Depends(get_db)):
    return await create_board(db, board)


@router.get("/", response_model=list[BoardRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_board(db)


@router.get("/{board_id}", response_model=BoardRead)
async def get_board(board_id: int, db: AsyncSession = Depends(get_db)):
    board = await get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="board not found")
    return board


@router.put("/{board_id}", response_model=BoardRead)
async def update_board(board_id: int, board: BoardUpdate,db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_manager)):
    updated = await update_board_by_id(db, board_id, board)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="board not found")
    return updated


@router.delete("/{board_id}")
async def delete_board(board_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_manager)):
    deleted = await deleted_board_by_id(db, board_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="board not found")
    return deleted