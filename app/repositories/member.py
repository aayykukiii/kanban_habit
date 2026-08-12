from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.member import Member, MemberRole
from app.models.users import User, UserRole
from app.schemas.member import MemberCreate, MemberUpdate


async def create_member(db: AsyncSession, member: MemberCreate):
    new_member = Member(
        full_name=member.full_name,
        email=member.email,
        role=member.role,
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)
    return new_member


async def get_all_member(db: AsyncSession):
    result = await db.execute(select(Member))
    return result.scalars().all()


async def get_member_by_id(db: AsyncSession, member_id: int):
    result = await db.execute(
        select(Member).where(Member.id == member_id)
    )
    return result.scalar_one_or_none()


async def update_member_by_id(
    db: AsyncSession,
    member_id: int,
    member_data: MemberUpdate,
    current_user: User,
):
    db_member = await get_member_by_id(db, member_id)

    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )

    update_data = member_data.model_dump(exclude_unset=True)

    if "role" in update_data and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only admin can change roles",
        )

    for field, value in update_data.items():
        setattr(db_member, field, value)

    await db.commit()
    await db.refresh(db_member)
    return db_member


async def delete_member_by_id(
    db: AsyncSession,
    member_id: int,
    current_user: User,
):
    db_member = await get_member_by_id(db, member_id)

    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only admin can delete members",
        )

    await db.delete(db_member)
    await db.commit()

    return {"detail": "member deleted"}