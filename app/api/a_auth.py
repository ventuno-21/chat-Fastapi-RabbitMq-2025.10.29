from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.m_user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.utils.deps import session
from app.utils.jwt import create_access_token
from app.utils.password import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, session=session):
    existing = await session.execute(select(User).where(User.username == user.username))
    if existing.scalar():
        raise HTTPException(
            status_code=400, detail="Username already exists, choose another one"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = session):
    result = await session.execute(select(User).where(User.username == user.username))
    db_user = result.scalar()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
