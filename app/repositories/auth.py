from sqlalchemy import select
from fastapi import HTTPException
from app.models.users import User
from app.core.security import hash_password, verify_password, create_access_token


async def register_user(db, user_data):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(400, "User already exists")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    await db.commit()
    return new_user


async def login_user(db, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(400, "User not found")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(400, "Wrong password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}