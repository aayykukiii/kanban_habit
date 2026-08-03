from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import PriorityTask, StatusType, TaskUpdate


async def create_task(db: AsyncSession, task: Task):
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_all_tasks(
    db: AsyncSession,
    search: Optional[str] = None,
    priority: Optional[PriorityTask] = None,
    status_type: Optional[StatusType] = None,
    column_id: Optional[int] = None,
    member_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0
):
    query = select(Task)
    if search:
        query = query.where(Task.title.ilike(f"%{search}%"))
    if priority:
        query = query.where(Task.priority == priority)
    if status_type:
        query = query.where(Task.status_type == status_type)
    if column_id:
        query = query.where(Task.column_id == column_id)
    if member_id:
        query = query.where(Task.member_id == member_id)
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().unique().all()


async def get_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().unique().one_or_none()


async def save_task(db: AsyncSession, task: Task):
    await db.commit()
    await db.refresh(task)
    return task


async def update_task_by_id(db: AsyncSession, task_id: int, task_data: TaskUpdate):
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    return await save_task(db, task)


async def delete_task_by_id(db: AsyncSession, task_id: int):
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return {"detail": "Task deleted"}