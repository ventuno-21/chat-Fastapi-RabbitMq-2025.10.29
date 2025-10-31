from sqlalchemy import String, Table, Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

group_user = Table(
    "group_user",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    image: Mapped[str] = mapped_column(String, nullable=True)  # base64
    users = relationship("User", secondary=group_user)
