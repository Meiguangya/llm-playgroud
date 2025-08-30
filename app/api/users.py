# app/api/users.py
from datetime import timedelta

import redis
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.db.session import SessionLocal
from app.core.security import hash_password, verify_password, create_access_token
from app.common.response import ApiResponse
from app.models import User
from app.schemas.user import *
from app.dependencies.get_current_user import get_current_user

import json

from app.core.redis_client import get_redis

router = APIRouter(prefix="/api/v1/users", tags=["users"])


# 依赖：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(
    request: LoginRequest = Body(...),
    db: Session = Depends(get_db),
    redis: redis.Redis = Depends(get_redis)
):
    # 1. 校验参数
    if not request.username or not request.password:
        return ApiResponse.fail(400, "缺少必填参数: username 或 password")

    # [可选] 验证码校验（此处省略，可集成 Redis 缓存验证码）

    # 2. 查询用户
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        # 为了安全，不区分“用户不存在”和“密码错误”
        return ApiResponse.fail(401, "用户名或密码错误")

    # 3. 校验密码
    if not verify_password(request.password, user.hashed_password):
        return ApiResponse.fail(401, "用户名或密码错误")

    # 4. 生成 Token
    access_token = create_token_and_store_in_redis(user,redis)

    # 5. 构造响应数据
    login_response = LoginResponse(
        token={
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600
        },
        user={
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "roles": ["user"]
        }
    )

    # 6. 更新最后登录时间（可选）
    user.last_login = datetime.utcnow()
    db.commit()

    return ApiResponse.success(login_response, "登录成功")



@router.post("/register", response_model=ApiResponse[dict])
def register_user(
    user_in: UserCreate = Body(...),
    db: Session = Depends(get_db),
    redis: redis.Redis = Depends(get_redis)
):
    """
    用户注册接口
    - **username**: 用户名（必填）
    - **password**: 密码（明文，后端自动加密）
    - **email**: 邮箱（可选）
    """
    # 检查用户名是否已存在
    existing_user_by_username = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing_user_by_username:
        return ApiResponse.fail(400, "用户名已存在")

    # 检查邮箱是否已存在（如果提供了邮箱）
    if user_in.email:
        existing_user_by_email = db.query(models.User).filter(models.User.email == user_in.email).first()
        if existing_user_by_email:
            return ApiResponse.fail(400, "该邮箱已被注册")

    # 创建新用户（密码加密）
    db_user = models.User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        email=user_in.email,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_token_and_store_in_redis(db_user,redis)

    return ApiResponse.success({
        "message": "注册成功",
        "user_id": db_user.id,
        "username": db_user.username,
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600
    })


def create_token_and_store_in_redis(user: models.User, redis: redis.Redis) -> str:
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "scopes": ["user"]
    }
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=60))

    redis_key = f"auth:token:{access_token}"
    redis_value = {
        "user_id": user.id,
        "username": user.username,
        "is_active": user.is_active
    }
    try:
        redis.setex(
            name=redis_key,
            time=3600,
            value=json.dumps(redis_value, ensure_ascii=False)
        )
    except Exception as e:
        print(f"⚠️ Redis 写入失败: {e}")

    return access_token


@router.post("/logout")
def logout(
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
        redis: redis.Redis = Depends(get_redis)
):
    """
    用户退出登录
    - 删除 Redis 中的 token 缓存
    - 返回成功响应
    """
    try:
        # Redis 中存储的 key，例如：token:123 或 session:user_123
        redis_key = f"auth:token:{current_user.token}"

        # 删除 Redis 中的 token
        deleted_count = redis.delete(redis_key)

        # 可选：记录用户最后登出时间
        # current_user.last_logout_at = datetime.now(timezone.utc)
        # db.commit()

        return ApiResponse.success(
            data=None,
            message="退出登录成功"
        )

    except Exception as e:
        return ApiResponse.fail(
            code=500,
            message="退出登录失败，请稍后重试"
        )