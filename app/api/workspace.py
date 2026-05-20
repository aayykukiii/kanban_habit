from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.users import User
from app.repositories.workspace import create_workspace, get_all_workspace, get_workspace_by_id, update_workspace_by_id, delete_workspace_by_id
from app.schemas.workspace import WorkSpaceCreate, WorkSpaceRead, WorkSpaceUpdate


router = APIRouter()


@router.post("/", response_model=WorkSpaceRead)
async def post_workspace(workspace: WorkSpaceCreate,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await create_workspace(db, workspace, user)


@router.get("/", response_model=list[WorkSpaceRead])
async def get_all(user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await get_all_workspace(db, user)


@router.get("/{workspace_id}", response_model=WorkSpaceRead)
async def get_workspace(workspace_id: int,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await get_workspace_by_id(db, workspace_id, user)


@router.put("/{workspace_id}", response_model=WorkSpaceRead)
async def update_workspace(workspace_id: int,workspace: WorkSpaceUpdate,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await update_workspace_by_id(db, workspace_id, workspace, user)


@router.delete("/{workspace_id}")
async def delete_workspace(workspace_id: int,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await delete_workspace_by_id(db, workspace_id, user)