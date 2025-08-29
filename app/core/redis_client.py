# app/core/redis_client.py
import redis
from typing import Optional
from fastapi import Depends, HTTPException, status

# 全局 Redis 客户端实例
redis_client: Optional[redis.Redis] = None

def init_redis():
    """初始化 Redis 客户端"""
    global redis_client
    try:

        redis_client = redis.Redis(
            host='192.168.3.195',  # 根据你的配置修改
            port=6379,
            password='123456',  # 如果设置了密码，填在这里；否则可删除此行
            db=0,
            decode_responses=True,  # ⭐ 非常重要！支持中文
            socket_connect_timeout=5,
            socket_timeout=5
        )

        # redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        # 测试连接
        redis_client.ping()
        print("✅ Redis 连接成功")
    except Exception as e:
        print(f"❌ Redis 连接失败: {e}")
        raise

def get_redis() -> redis.Redis:
    """FastAPI 依赖：获取 Redis 客户端"""
    if redis_client is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Redis 未初始化"
        )
    return redis_client