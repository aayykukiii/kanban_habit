from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.tag import TagCreate, TagUpdate
from app.models.tag import Tag
from fastapi import HTTPException, status


async def create_tag(db: AsyncSession, tag: TagCreate):
    new_tag = Tag(
        name=tag.name,
        color=tag.color
    )
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag


async def get_all_tag(db: AsyncSession):
    result = await db.execute(select(Tag))
    return result.scalars().all()


async def get_tag_by_id(db: AsyncSession, tag_id: int):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    return result.scalar_one_or_none()


async def update_tag_by_id(db: AsyncSession, tag_id: int, tag_data: TagUpdate):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    db_tag = result.scalar_one_or_none()
    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='tag not found')
    update_data = tag_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_tag, key, value)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag


async def delete_tag_by_id(db: AsyncSession, tag_id: int):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    db_tag = result.scalar_one_or_none()
    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='tag not found')
    await db.delete(db_tag)
    await db.commit()
    return {'detail': 'tag deleted'}
