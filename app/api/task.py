from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.task_service import move_task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, PriorityTask, StatusType
from app.repositories.task import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task_by_id,
    delete_task_by_id
)

router = APIRouter()


@router.post('/', response_model=TaskRead)
async def post_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task)


@router.get('/', response_model=list[TaskRead])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    search: str | None = None,
    priority: PriorityTask | None = None,
    status_type: StatusType | None = None,
    column_id: int | None = None,
    member_id: int | None = None,
    limit: int = 50,
    offset: int = 0
):
    return await get_all_tasks(
        db,
        search,
        priority,
        status_type,
        column_id,
        member_id,
        limit,
        offset
    )


@router.get('/{task_id}', response_model=TaskRead)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await get_task_by_id(db, task_id)


@router.put('/{task_id}', response_model=TaskRead)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await update_task_by_id(db, task_id, task)


@router.patch('/{task_id}/move', response_model=TaskRead)
async def move_task_endpoint(
    task_id: int,
    new_column_id: int,
    new_position: int,
    db: AsyncSession = Depends(get_db)
):
    return await move_task(db, task_id, new_column_id, new_position)


@router.delete('/{task_id}')
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_task_by_id(db, task_id)