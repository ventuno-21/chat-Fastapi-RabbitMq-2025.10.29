from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from app.utils.jwt import verify_token
from app.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.models.m_user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]


async def get_current_admin(
    username: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one()
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# instead od using          => session: AsyncSession = Depends(get_session)
# with below dependency use => session: SessionDep
SessionDep = Annotated[AsyncSession, Depends(get_session)]
