from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import (
    get_current_admin,
    get_current_user,
)
from app.core.db import get_db
from app.models.users import User
from app.repositories.auth import (
    login_user,
    register_user,
    update_user_role,
)
from app.schemas.users import (
    UserCreate,
    UserRead,
    UserRoleUpdate,
)


router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
)
async def register(
    user: UserCreate,
    db=Depends(get_db),
):
    """
    Регистрация.

    Каждый новый пользователь
    автоматически получает USER.
    """

    return await register_user(
        db,
        user,
    )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    """
    Авторизация.

    OAuth2 использует username,
    но в нашем случае username = email.
    """

    return await login_user(
        db,
        form_data.username,
        form_data.password,
    )


@router.get(
    "/me",
    response_model=UserRead,
)
async def get_me(
    user: User = Depends(get_current_user),
):
    """
    Информация о текущем пользователе.
    """

    return user


@router.patch(
    "/users/{user_id}/role",
    response_model=UserRead,
)
async def change_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db=Depends(get_db),
    admin: User = Depends(get_current_admin),
):

    return await update_user_role(
        db,
        user_id,
        data.role,
    )