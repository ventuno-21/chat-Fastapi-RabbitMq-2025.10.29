from sqlalchemy import ForeignKey, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )  # for private
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"), nullable=True)
    content: Mapped[str] = mapped_column(String, nullable=True)
    file_base64: Mapped[str] = mapped_column(String, nullable=True)
    is_image: Mapped[bool] = mapped_column(Boolean, default=False)
    self_destruct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    file_base64: Mapped[str] = mapped_column(String, nullable=True)
    is_image: Mapped[bool] = mapped_column(Boolean, default=False)
    self_destruct: Mapped[bool] = mapped_column(Boolean, default=False)
