from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task


async def move_task(
    db: AsyncSession,
    task_id: int,
    new_column_id: int,
    new_position: int
):
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        return None

    old_column_id = task.column_id
    old_position = task.position

    if old_column_id == new_column_id:

        if new_position > old_position:
            await db.execute(
                update(Task)
                .where(
                    Task.column_id == new_column_id,
                    Task.position > old_position,
                    Task.position <= new_position
                )
                .values(position=Task.position - 1)
            )
        else:
            await db.execute(
                update(Task)
                .where(
                    Task.column_id == new_column_id,
                    Task.position >= new_position,
                    Task.position < old_position
                )
                .values(position=Task.position + 1)
            )

    else:
        await db.execute(
            update(Task)
            .where(
                Task.column_id == old_column_id,
                Task.position > old_position
            )
            .values(position=Task.position - 1)
        )

        await db.execute(
            update(Task)
            .where(
                Task.column_id == new_column_id,
                Task.position >= new_position
            )
            .values(position=Task.position + 1)
        )

    task.column_id = new_column_id
    task.position = new_position

    await db.commit()
    await db.refresh(task)

    return task