from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.task import Task
from app.models.tag import Tag
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, task: TaskCreate):
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status_type=task.status_type,
        position=task.position,
        column_id=task.column_id,
        member_id=task.member_id,
        start_date=task.start_date,
        deadline=task.deadline,
        estimated_time=task.estimated_time,
        actual_time=task.actual_time,
        is_blocked=task.is_blocked,
        blocked_reason=task.blocked_reason
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task



async def get_all_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().unique().all()

async def get_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.unique().scalar_one_or_none()


async def update_task_by_id(db: AsyncSession, task_id: int, task_data: TaskUpdate):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.unique().scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='task not found')
    update_data = task_data.model_dump(exclude_unset=True)

    if 'tag_ids' in update_data:
        tag_ids = update_data.pop('tag_ids')
        if tag_ids:
            result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
            tags = result.scalars().all()
            db_task.tags = tags
        else:
            db_task.tags = []

    for field, value in update_data.items():
        setattr(db_task, field, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task



async def delete_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='task not found')
    await db.delete(db_task)
    await db.commit()
    return {'detail': 'task deleted'}