import redis.asyncio as redis
from langgraph.checkpoint.redis.aio import AsyncRedisSaver

_saver = None

async def get_redis_checkpointer():
    global _saver
    if _saver is None:
        print("创建开始--->AsyncRedisSaver...")
        redis_client = redis.Redis(
            host='192.168.3.195',
            port=6379,
            password='123456',
            db=0,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        _saver = AsyncRedisSaver(redis_client=redis_client)
        await _saver.asetup()
        print("创建结束--->AsyncRedisSaver...")
    return _saver