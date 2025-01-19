from typing import Optional
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    user_email: Mapped[str] = mapped_column(String(50)) 
    user_pass: Mapped[str] = mapped_column(String())

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_chats: Mapped[Optional["UserChats"]] = relationship(backref="userChats.user_chat_id", passive_deletes=True)


class UserChats(Base):
    __tablename__ = "userChats"
    user_chat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_prompt: Mapped[str] = mapped_column(String(),nullable=True)
    bot_response: Mapped[str] = mapped_column(String())
    chat_image: Mapped[str] = mapped_column(String(),nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))