from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.workspace import WorkSpace
from app.models.users import User
from app.schemas.workspace import WorkSpaceCreate, WorkSpaceUpdate


async def create_workspace(db: AsyncSession, workspace: WorkSpaceCreate, user: User):
    new_workspace = WorkSpace(
        name=workspace.name,
        description=workspace.description,
        owner_id=user.id
    )
    db.add(new_workspace)
    await db.commit()
    await db.refresh(new_workspace)
    return new_workspace


async def get_all_workspace(db: AsyncSession, user: User):
    if user.role == "admin":
        stmt = select(WorkSpace)
    else:
        stmt = select(WorkSpace).where(WorkSpace.owner_id == user.id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_workspace_by_id(db: AsyncSession, workspace_id: int, user: User):
    stmt = select(WorkSpace).where(WorkSpace.id == workspace_id)
    if user.role != "admin":
        stmt = stmt.where(WorkSpace.owner_id == user.id)
    result = await db.execute(stmt)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="workspace not found"
        )

    return workspace

 
async def update_workspace_by_id(db: AsyncSession, workspace_id: int, workspace_data: WorkSpaceUpdate, user: User):
    workspace = await get_workspace_by_id(db, workspace_id, user)
    update_data = workspace_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workspace, key, value)
    await db.commit()
    await db.refresh(workspace)
    return workspace


async def delete_workspace_by_id(db: AsyncSession, workspace_id: int):
    result = await db.execute(select(WorkSpace).where(WorkSpace.id == workspace_id))
    db_workspace = result.scalar_one_or_none()
    if not db_workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='worksapce not found')
    await db.delete(db_workspace)
    await db.commit()
    return {'detail': 'workspace deleted'}