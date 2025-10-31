import base64
from datetime import timedelta

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.m_user import User
from app.schemas.s_user import UserCreate, UserLogin, UserOut
from app.services.image_utils import resize_base64_image
from app.utils.deps import get_current_user, session
from app.utils.email import send_reset_email
from app.utils.jwt import create_access_token, verify_token
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


@router.post("/upload-profile")
async def upload_profile_image(
    file: UploadFile = File(...),
    session: AsyncSession = session,
    username: str = Depends(get_current_user),
):
    """
    Upload and update a user's profile image in the database.

    This endpoint accepts an image file, converts it to base64, resizes it to reduce size,
    and stores the resulting base64 string in the user's profile record.

    Args:
        file (UploadFile): The uploaded image file (e.g., JPEG or PNG).
        session (AsyncSession): The active SQLAlchemy async session used for database operations.
        username (str): The username of the currently authenticated user, obtained via dependency injection.

    Returns:
        dict: A message confirming successful upload, e.g. {"message": "Profile image updated"}.

    Example:
        >>> # Example request using HTTPie or curl:
        >>> # HTTPie
        >>> http -f POST http://localhost:8000/upload-profile \
        ... "Authorization: Bearer <ACCESS_TOKEN>" \
        ... file@profile.jpg
        >>>
        >>> # Example JSON response:
        >>> {"message": "Profile image updated"}
    """

    # Read the uploaded file's binary content
    content = await file.read()

    # Convert the binary image to a base64 string
    base64_str = base64.b64encode(content).decode("utf-8")

    # Resize/compress the image to stay under the allowed size limit
    resized = resize_base64_image(base64_str)

    # Retrieve the user record by username from the database
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one()

    # Update the user's profile image with the resized base64 string
    user.profile_image = resized

    # Commit the change to the database
    await session.commit()

    # Return a success message
    return {"message": "Profile image updated"}


Query


@router.post("/request-reset")
async def request_reset(email: EmailStr, session=session):
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token(
        {"sub": user.username}, expires_delta=timedelta(minutes=15)
    )
    send_reset_email(email, token)
    return {"message": "Reset link sent"}


@router.post("/reset-password")
async def reset_password(
    token: str = Query(...),
    new_password: str = Query(...),
    session: AsyncSession = session,
):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    result = await session.execute(select(User).where(User.username == payload["sub"]))
    user = result.scalar_one()
    user.hashed_password = hash_password(new_password)
    await session.commit()
    return {"message": "Password updated"}
