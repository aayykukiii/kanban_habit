from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate
from fastapi import HTTPException, status
import enum


class MemberRole(enum.Enum):
    member = 'member'
    viewer = 'viewer'
    admin = 'admin'


async def create_member(db: AsyncSession, member: MemberCreate):
    new_member = Member (
        full_name=member.full_name,
        email=member.email,
        role=member.role.value
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)
    return new_member



async def get_all_member(db: AsyncSession):
    result = await db.execute(select(Member))
    return result.scalars().all()



async def get_member_by_id(db: AsyncSession, member_id: int):
    result = await db.execute(select(Member).where(Member.id == member_id))
    return result.scalar_one_or_none()


async def update_member_by_id(db: AsyncSession, member_id: int, member_data: MemberUpdate, current_user: Member):
    result = await db.execute(select(Member).where(Member.id == member_id))
    db_member = result.scalar_one_or_none()
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='member not found')
    update_data = member_data.model_dump(exclude_unset=True)
    if 'role' in update_data:
        if current_user.role != MemberRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='only admin can change roles'
            )
        if db_member.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='admin cannot change own role'
            )
    for field, value in update_data.items():
        setattr(db_member, field, value)
    await db.commit()
    await db.refresh(db_member)
    return db_member

async def delete_member_by_id(db: AsyncSession, member_id: int, current_user: Member):
    result = await db.execute(select(Member).where(Member.id == member_id))
    db_member = result.scalar_one_or_none()
    if not db_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='member not found')
    if current_user.role != MemberRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only admin can delete members')
    if db_member.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='you cannot delete yourself')
    if db_member.role == MemberRole.admin:
        result = await db.execute(select(Member).where(Member.role == MemberRole.admin))
        admins = result.scalars().all()
        if len(admins) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='cannot delete the last admin'
            )
    await db.delete(db_member)
    await db.commit()
    return {'detail': 'member deleted'}