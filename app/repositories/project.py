from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import Project
from fastapi import HTTPException, status


async def create_project(db: AsyncSession, project: ProjectCreate):
    new_project = Project(
        title=project.title,
        description=project.description,
        workspace_id=project.workspace_id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


async def get_all_project(db: AsyncSession):
    result = await db.execute(select(Project))
    return result.scalars().all()


async def get_project_by_id(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()



async def update_project_by_id(db: AsyncSession, project_id: int, project_data: ProjectUpdate):
    result = await db.execute(select(Project).where(Project.id == project_id))
    db_project = result.scalar_one_or_none()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='project not found')
    update_data = project_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    await db.commit()
    await db.refresh(db_project)
    return db_project



async def delete_project_by_id(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    db_project = result.scalar_one_or_none()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='project not found')
    await db.delete(db_project)
    await db.commit()
    return {'detail': 'project deleted'}