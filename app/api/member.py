from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.member import (create_member, get_all_member, get_member_by_id,
                                 update_member_by_id, delete_member_by_id)
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.member import MemberCreate, MemberRead, MemberUpdate


router = APIRouter()


@router.post('/member', response_model=MemberRead)
async def post_member(member: MemberCreate, db: AsyncSession = Depends(get_db)):
    return await create_member(db, member)



@router.get('/member', response_model=list[MemberRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_member(db)


@router.get('/member/{member_id}', response_model=MemberRead)
async def get_member(member_id: int, db: AsyncSession = Depends(get_db)):
    member = await get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='member not found')
    return member



@router.put('/member/{member_id}', response_model=MemberUpdate)
async def update_member(member_id: int, member: MemberUpdate, db: AsyncSession = Depends(get_db)):
    return await update_member_by_id(db, member_id, member)


@router.delete('/member/{member_id}')
async def delete_member(member_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_member_by_id(db, member_id)