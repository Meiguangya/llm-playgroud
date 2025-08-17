# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# 创建用户时用的 Schema
class UserCreate(BaseModel):
    username: str
    password: str  # 明文密码（仅用于接收，不会返回）
    email: Optional[EmailStr] = None


# 更新用户信息
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


# 返回给前端的用户信息（不含密码）
class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True  # 支持 ORM 模式（新版 Pydantic 使用 from_attributes）