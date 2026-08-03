from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.users import User, UserRole
from app.schemas.task import TaskCreate

from app.repositories.task import (
    create_task as create_task_repo,
    get_task_by_id,
    save_task,
    delete_task_by_id,
)


def check_task_permission(task: Task, current_user: User):
    if current_user.role == UserRole.ADMIN:
        return
    if task.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")


async def create_task(db: AsyncSession, task_data: TaskCreate, current_user: User):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status_type=task_data.status_type,
        position=task_data.position,
        column_id=task_data.column_id,
        member_id=task_data.member_id,
        start_date=task_data.start_date,
        deadline=task_data.deadline,
        estimated_time=task_data.estimated_time,
        actual_time=task_data.actual_time,
        is_blocked=task_data.is_blocked,
        blocked_reason=task_data.blocked_reason,
        author_id=current_user.id,
    )
    return await create_task_repo(db, task)


async def move_task(db: AsyncSession, task_id: int, new_column_id: int, new_position: int, current_user: User):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.unique().scalar_one_or_none()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        ) 
    check_task_permission(task, current_user)
    old_column_id = task.column_id
    old_position = task.position
    if old_column_id == new_column_id:
        if new_position > old_position:
            await db.execute(
                update(Task)
                .where(
                    Task.column_id == new_column_id,
                    Task.position > old_position,
                    Task.position <= new_position,
                )
                .values(position=Task.position - 1)
            )
        elif new_position < old_position:
            await db.execute(
                update(Task)
                .where(
                    Task.column_id == new_column_id,
                    Task.position >= new_position,
                    Task.position < old_position,
                )
                .values(position=Task.position + 1)
            )
    else:
        await db.execute(
            update(Task)
            .where(
                Task.column_id == old_column_id,
                Task.position > old_position,
            )
            .values(position=Task.position - 1)
        )
        await db.execute(
            update(Task)
            .where(
                Task.column_id == new_column_id,
                Task.position >= new_position,
            )
            .values(position=Task.position + 1)
        )
    task.column_id = new_column_id
    task.position = new_position
    await db.commit()
    await db.refresh(task)
    return task


from app.repositories.task import (
    get_task_by_id,
    save_task,
    delete_task_by_id,
)

from app.schemas.task import TaskUpdate


async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User,
):
    task = await get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    check_task_permission(task, current_user)

    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    return await save_task(db, task)


async def delete_task(
    db: AsyncSession,
    task_id: int,
    current_user: User,
):
    task = await get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    check_task_permission(task, current_user)

    return await delete_task_by_id(db, task_id)