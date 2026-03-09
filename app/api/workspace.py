from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.workspace import (create_workspace, get_all_workspace, get_workspace_by_id,
                                    update_workspace_by_id, delete_workspace_by_id)
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base
from app.schemas.workspace import WorkSpaceCreate, WorkSpaceRead, WorkSpaceUpdate


router = APIRouter()


@router.post('/workspace', response_model=WorkSpaceRead)
async def post_workspace(workspace: WorkSpaceCreate, db: AsyncSession = Depends(get_db)):
    return await create_workspace(db, workspace)



@router.get('/workspace', response_model=list[WorkSpaceRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_workspace(db)


@router.get('/workspace/{workspace_id}', response_model=WorkSpaceRead)
async def get_workspace(workspace_id: int, db: AsyncSession = Depends(get_db)):
    workspace = await get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='member not found')
    return workspace


@router.put('/workspace/{workspace_id}', response_model=WorkSpaceUpdate)
async def update_workspace(workspace_id: int, workspace: WorkSpaceUpdate, db: AsyncSession = Depends(get_db)):
    return await update_workspace_by_id(db, workspace_id, workspace)


@router.delete('/workspace/{workspace_id}')
async def delete_workspace(workspace_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_workspace_by_id(db, workspace_id)