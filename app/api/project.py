from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.project import (create_project, get_all_project,
                                  get_project_by_id, update_project_by_id, delete_project_by_id)
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate


router = APIRouter()


@router.post('/project', response_model=ProjectRead)
async def post_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await create_project(db, project)



@router.get('/project', response_model=list[ProjectRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_project(db)


@router.get('/project/{project_id}', response_model=ProjectRead)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='project not found')
    return project


@router.put('/project/{project_id}', response_model=ProjectUpdate)
async def update_project(project_id: int, project: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    return await update_project_by_id(db, project_id, project)


@router.delete('/project/{project_id}')
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_project_by_id(db, project_id)