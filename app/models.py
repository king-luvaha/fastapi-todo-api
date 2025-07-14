from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timedelta

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)  # 👈 Add this line
    hashed_password = Column(String(100), nullable=False)

    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="not_done")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", backref="refresh_tokens")
