# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"