from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ChannelUser(Base):
    __tablename__ = "channel_user"

    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    image: Mapped[str] = mapped_column(String, nullable=True)  # base64

    users = relationship("User", secondary="channel_user", back_populates="channels")
