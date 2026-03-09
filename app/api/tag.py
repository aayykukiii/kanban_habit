from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.tag import (create_tag, get_all_tag, get_tag_by_id,
                              update_tag_by_id, delete_tag_by_id)
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from app.schemas.tag import TagCreate, TagRead, TagUpdate


router = APIRouter()


@router.post('/tag', response_model=TagRead)
async def post_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    return await create_tag(db, tag)


@router.get('/tag', response_model=list[TagRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_tag(db)


@router.get('/tag/{tag_id}', response_model=TagRead)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='tag not found')
    return tag


@router.put('/tag/{tag_id}', response_model=TagUpdate)
async def update_tag(tag_id: int, tag: TagUpdate, db: AsyncSession = Depends(get_db)):
    return await update_tag_by_id(db, tag_id, tag)


@router.delete('/tag/{tag_id}')
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_tag_by_id(db, tag_id)