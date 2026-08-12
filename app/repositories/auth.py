from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.users import User, UserRole
from app.schemas.users import UserCreate


async def register_user(
    db: AsyncSession,
    user_data: UserCreate,
) -> User:
    """
    Регистрирует нового пользователя.

    Новый пользователь всегда получает роль USER.
    """

    result = await db.execute(
        select(User).where(
            User.email == user_data.email
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = User(
        email=user_data.email,
        hashed_password=hash_password(
            user_data.password
        ),
        role=UserRole.USER.value,
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


async def login_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> dict:
    """
    Авторизует пользователя.

    Email используется как username
    в OAuth2PasswordRequestForm.
    """

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


async def update_user_role(
    db: AsyncSession,
    user_id: int,
    role: UserRole,
) -> User:
    """
    Меняет роль пользователя.

    Вызывать эту функцию может только ADMIN.
    Проверка ADMIN находится в get_current_admin().
    """

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.role = role.value

    await db.commit()
    await db.refresh(user)

    return user