from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.task import (create_task, get_all_tasks, get_task_by_id,
                               update_task_by_id, delete_task_by_id)
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


router = APIRouter()


@router.post('/task', response_model=TaskRead)
async def post_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task)


@router.get('/task', response_model=list[TaskRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_tasks(db)


@router.get('/task/{task_id}', response_model=TaskRead)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='tag not found')
    return task


@router.put('/task/{task_id}', response_model=TaskUpdate)
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    return await update_task_by_id(db, task_id, task)


@router.delete('/task/{task_id}')
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_task_by_id(db, task_id)