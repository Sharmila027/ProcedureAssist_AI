from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import TokenResponse, UserLogin, UserRegister


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        preferred_language=user_data.preferred_language,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "preferred_language": user.preferred_language,
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )

    user = result.scalar_one_or_none()

    if not user or not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(user.id)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        preferred_language=user.preferred_language,
    )