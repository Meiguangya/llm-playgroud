# app/dependencies/get_current_user.py
from fastapi import Request, Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from app.core.redis_client import get_redis
from app.schemas.user import CurrentUser
from app.core.security import decode_access_token
import json
import redis

security = HTTPBearer()

async def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)],
    redis: Annotated[redis.Redis, Depends(get_redis)]
) -> CurrentUser:
    """
    依赖函数：获取当前用户
    - 验证 Bearer Token
    - 解码 JWT
    - 校验 Redis 中是否存在该 token（确认有效性）
    - 使用 request.state 实现“类 ThreadLocal”缓存
    """
    token = credentials.credentials

    # 1. 检查是否已在本次请求中解析过（类 ThreadLocal 缓存）
    if hasattr(request.state, "current_user"):
        return request.state.current_user

    # 2. 解码 JWT Token
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效或过期的 Token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = payload.get("sub")
        username = payload.get("username")
        if not user_id or not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token 中缺少用户信息",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token 解析失败: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 校验 Redis 中是否存在该 token
    redis_key = f"auth:token:{token}"
    token_data = redis.get(redis_key)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已被登出",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. 解析用户信息（可选：从 Redis 数据中读取，或直接用 payload）
    try:
        data = json.loads(token_data)
        user_id = int(data["user_id"])
        username = data["username"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 数据格式错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 5. 创建 CurrentUser 对象
    current_user = CurrentUser(user_id=user_id, username=username)

    # 6. 存入 request.state（实现“类 ThreadLocal”效果）
    if not hasattr(request.state, "current_user"):
        request.state.current_user = current_user

    return current_user