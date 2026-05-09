from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.workspace import (
    create_workspace,
    get_all_workspace,
    get_workspace_by_id,
    update_workspace_by_id,
    delete_workspace_by_id
)
from app.schemas.workspace import WorkSpaceCreate, WorkSpaceRead, WorkSpaceUpdate


router = APIRouter()


@router.post('/', response_model=WorkSpaceRead)
async def post_workspace(
    workspace: WorkSpaceCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_workspace(db, workspace)


@router.get('/', response_model=list[WorkSpaceRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_workspace(db)


@router.get('/{workspace_id}', response_model=WorkSpaceRead)
async def get_workspace(workspace_id: int, db: AsyncSession = Depends(get_db)):
    workspace = await get_workspace_by_id(db, workspace_id)

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='workspace not found'
        )

    return workspace


@router.put('/{workspace_id}', response_model=WorkSpaceRead)
async def update_workspace(
    workspace_id: int,
    workspace: WorkSpaceUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_workspace_by_id(db, workspace_id, workspace)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='workspace not found'
        )

    return updated


@router.delete('/{workspace_id}')
async def delete_workspace(workspace_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_workspace_by_id(db, workspace_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='workspace not found'
        )

    return {'detail': 'workspace deleted'}