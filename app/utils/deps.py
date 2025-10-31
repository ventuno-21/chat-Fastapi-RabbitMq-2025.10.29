from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_token
from app.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]


# session: AsyncSession = Depends(get_session)
SessionDep = Annotated[AsyncSession, Depends(get_session)]
