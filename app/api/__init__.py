from .board import router as board_router
from .column import router as column_router
from .member import router as member_router
from .project import router as project_router
from .tag import router as tag_router
from .task import router as task_router
from .workspace import router as workspace_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(board_router)
router.include_router(column_router)
router.include_router(member_router)
router.include_router(project_router)
router.include_router(tag_router)
router.include_router(task_router)
router.include_router(workspace_router)