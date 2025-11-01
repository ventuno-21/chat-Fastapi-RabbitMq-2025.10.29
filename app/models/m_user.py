from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class UserBlock(Base):
    __tablename__ = "user_block"

    blocker_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    blocked_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    blocked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_image: Mapped[str] = mapped_column(String, nullable=True)  # base64
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    channels = relationship("Channel", secondary="channel_user", back_populates="users")
    groups = relationship("Group", secondary="group_user", back_populates="users")
    blocked_users = relationship(
        "User",
        secondary="user_block",
        primaryjoin=id == UserBlock.blocker_id,
        secondaryjoin=id == UserBlock.blocked_id,
        backref="blocked_by",
    )
