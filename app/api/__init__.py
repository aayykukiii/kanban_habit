from fastapi import APIRouter

from .board import router as board_router
from .column import router as column_router
from .member import router as member_router
from .project import router as project_router
from .tag import router as tag_router
from .task import router as task_router
from .workspace import router as workspace_router
from .auth import router as auth_router


router = APIRouter()

router.include_router(board_router, prefix='/boards', tags=['Boards'])
router.include_router(column_router, prefix='/columns', tags=['Columns'])
router.include_router(member_router, prefix="/members", tags=["Members"])
router.include_router(project_router, prefix='/projects', tags=['Projects'])
router.include_router(tag_router, prefix='/tags', tags=['Tags'])
router.include_router(task_router, prefix='/tasks', tags=['Tasks'])
router.include_router(workspace_router, prefix='/workspaces', tags=['Workspaces'])
router.include_router(auth_router, prefix='/auth', tags=['Auth'])