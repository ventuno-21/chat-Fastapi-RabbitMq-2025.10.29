from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import String, JSON


class User(SQLModel, table=True):
    """User model - stores account information."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(
        sa_column=Column("username", String, unique=True, nullable=False)
    )
    email: str = Field(sa_column=Column("email", String, unique=True, nullable=False))
    hashed_password: str
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    profile_avatar_b64: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tokens: List["EmailVerificationToken"] = Relationship(back_populates="user")


class EmailVerificationToken(SQLModel, table=True):
    """Stores activation tokens for user verification."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=24)
    )

    user: Optional[User] = Relationship(back_populates="tokens")
