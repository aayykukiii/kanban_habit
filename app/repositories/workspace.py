from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.workspace import WorkSpace
from app.schemas.workspace import WorkSpaceCreate, WorkSpaceUpdate
from fastapi import HTTPException, status



async def create_workspace(db: AsyncSession, workspace: WorkSpaceCreate):
    new_workspase = WorkSpace(
        name=workspace.name,
        description=workspace.description
    )
    db.add(new_workspase)
    await db.commit()
    await db.refresh(new_workspase)
    return new_workspase



async def get_all_workspace(db: AsyncSession):
    result = await db.execute(select(WorkSpace))
    return result.scalars().all()



async def get_workspace_by_id(db: AsyncSession, workspace_id: int):
    result = await db.execute(select(WorkSpace).where(WorkSpace.id == workspace_id))
    return result.scalar_one_or_none()


async def update_workspace_by_id(db: AsyncSession, workspace_id: int, workspace_data: WorkSpaceUpdate):
    result = await db.execute(select(WorkSpace).where(WorkSpace.id == workspace_id))
    db_workspace = result.scalar_one_or_none()
    if not db_workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='worksapce not found')
    update_data = workspace_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_workspace, key, value)
    await db.commit()
    await db.refresh(db_workspace)
    return db_workspace


async def delete_workspace_by_id(db: AsyncSession, workspace_id: int):
    result = await db.execute(select(WorkSpace).where(WorkSpace.id == workspace_id))
    db_workspace = result.scalar_one_or_none()
    if not db_workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='worksapce not found')
    await db.delete(db_workspace)
    await db.commit()
    return {'detail': 'workspace deleted'}