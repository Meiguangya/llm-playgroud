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



# 登录请求
class LoginRequest(BaseModel):
    username: str
    password: str

# Token 响应
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None  # 可选：支持刷新

# 用户信息响应
class UserResponse(BaseModel):
    user_id: int
    username: str
    nickname: Optional[str] = None
    email: str
    avatar: Optional[str] = None
    is_active: bool
    roles: list[str]

# 登录成功返回的数据结构
class LoginResponse(BaseModel):
    token: Token
    user: UserResponse


class CurrentUser:
    """
    当前登录用户信息，用于在请求中传递
    类似 Java 中的 ThreadLocal<User>
    """
    def __init__(self, user_id: int, username: str, is_active: bool = True):
        self.user_id = user_id
        self.username = username
        self.is_active = is_active
        self.is_authenticated = True  # 标记为已认证

    def __repr__(self):
        return f"<CurrentUser id={self.user_id} username={self.username}>"