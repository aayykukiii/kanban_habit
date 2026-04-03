from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.users import UserCreate, UserRead
from app.repositories.auth import register_user, login_user
from app.api.deps import get_current_user
from app.core.db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db=Depends(get_db)):
    return await register_user(db, user)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    return await login_user(db, form_data.username, form_data.password)


@router.get("/me", response_model=UserRead)
async def get_me(user=Depends(get_current_user)):
    return user