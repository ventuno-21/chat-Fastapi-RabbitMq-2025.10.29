from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

channel_user = Table(
    "channel_user",
    Base.metadata,
    Column("channel_id", ForeignKey("channels.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    image: Mapped[str] = mapped_column(String, nullable=True)  # base64
    users = relationship("User", secondary=channel_user)
