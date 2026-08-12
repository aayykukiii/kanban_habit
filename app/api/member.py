from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.users import User
from app.repositories.member import (
    create_member,
    get_all_member,
    get_member_by_id,
    update_member_by_id,
    delete_member_by_id,
)
from app.schemas.member import MemberCreate, MemberRead, MemberUpdate


router = APIRouter()


@router.post("/", response_model=MemberRead)
async def post_member(
    member: MemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_member(db, member)


@router.get("/", response_model=list[MemberRead])
async def get_all(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_all_member(db)


@router.get("/{member_id}", response_model=MemberRead)
async def get_member(
    member_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = await get_member_by_id(db, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )

    return member


@router.put("/{member_id}", response_model=MemberRead)
async def update_member(
    member_id: int,
    member: MemberUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = await update_member_by_id(
        db,
        member_id,
        member,
        current_user,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )

    return updated


@router.delete("/{member_id}")
async def delete_member(
    member_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await delete_member_by_id(
        db,
        member_id,
        current_user,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )

    return deleted