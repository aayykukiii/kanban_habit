from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.board import BoardCreate, BoardUpdate
from app.models.board import Board
from fastapi import HTTPException, status


async def create_board(db: AsyncSession, board: BoardCreate):
    new_board = Board(
        title=board.title,
        description=board.description
    )
    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)
    return new_board


async def get_all_board(db: AsyncSession):
    result = await db.execute(select(Board))
    return result.scalars().all()


async def get_board_by_id(db: AsyncSession, board_id: int):
    result = await db.execute(select(Board).where(Board.id == board_id))
    return result.scalar_one_or_none()


async def update_board_by_id(db: AsyncSession, board_id: int, board_data: BoardUpdate):
    result = await db.execute(select(Board).where(Board.id == board_id))
    db_board = result.scalar_one_or_none()
    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='board not found')
    if db_board.is_archived:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid board')
    update_data = board_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_board, key, value)
    await db.commit()
    await db.refresh(db_board)
    return db_board


async def deleted_board_by_id(db: AsyncSession, board_id: int):
    result = await db.execute(select(Board).where(Board.id == board_id))
    db_board = result.scalar_one_or_none()
    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='board not found')
    if db_board.is_archived:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid board')
    db_board.is_archived = True
    await db.commit()
    return {'detail': 'board deactivated'}