from sqlalchemy.orm import Session
from schemas.board import BoardCreate, BoardRead, BoardUpdate
from models.board import Board
from fastapi import HTTPException, status




def create_board(db: Session, board: BoardCreate):
    new_board = Board(
        title=board.title,
        description=board.description
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board


def get_all_board(db: Session):
    return db.query(Board).all()


def get_board_by_id(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()


def update_board_by_id(db: Session, board_id: int, board_data: BoardUpdate):
    db_board = db.query(Board).filter(Board.id == board_id).first()
    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='board not found')
    if db_board.is_archived:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid board')
    update_data = board_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_board, key, value)
    db.commit()
    db.refresh(db_board)
    return db_board



def deleted_board_by_id(db: Session, board_id: int):
    db_board = db.query(Board).filter(Board.id == board_id).first()
    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='board not found')
    if db_board.is_archived:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid board')
    db_board.is_archived = True
    db.commit()
    return {'detail': 'board deactivated'}