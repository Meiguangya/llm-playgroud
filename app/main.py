# 应用入口
from contextlib import asynccontextmanager

# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging

logger = logging.getLogger(__name__)

# 导入 API 路由
from app.api.users import router as users_router
from app.api.dashscope import router as dashscope_router
from app.api.chat import router as ai_chat_router
from app.api.rag import router as rag_router
from app.chroma.chroma_client import ChromaSingleton
from app.api.chroma_router import router as chroma_router
from app.api.chat_v2 import router as chat_v2_router
from app.api.employee import router as employee_router
from app.api.chat_conversations import router as chat_conversations_router
from app.api.chat_message import router as chat_message_router

# 导入一些初始化方法
import os
from app.core.redis_client import init_redis
from app.ai.rag.loader.load_system_file import LoadSystemFile
from app.ai.checkpoint.redis_checkpoint import get_redis_checkpointer


@asynccontextmanager
async def lifespan(app: FastAPI):

    # 初始化redis
    print("Initializing Redis client start...")
    init_redis()
    print("Initializing Redis client end...")

    # 初始化redis_checkpoint
    print("Initializing Redis CheckPoint start...")
    await get_redis_checkpointer()
    print("Initializing Redis CheckPoint end...")

    # 应用启动时初始化 Chroma 客户端
    # print("Initializing Chroma client...")
    # ChromaSingleton.get_vectorstore()  # 触发初始化
    # logger.info("Chroma 客户端初始化成功")
    #
    # print("将数据加载到chroma中")
    #
    # # 加个配置
    # load_system_doc = os.getenv("LOAD_SYSTEM_DOCUMENT", "false").lower()
    # print(f"load_system_doc:[{load_system_doc}]")
    # if load_system_doc == 'true':
    #     LoadSystemFile.load_system_file()
    # else:
    #     print("未开启加载系统文档")

    yield
    logger.info("应用关闭中...")

    # 释放资源

    print("👋 资源释放完成，应用已关闭")


# 创建 FastAPI 实例
app = FastAPI(
    title="My FastAPI Project",
    description="A sample FastAPI project with structured directory layout.",
    version="0.1.0",
    lifespan=lifespan
)

# 配置 CORS（可选，用于前端跨域请求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应更严格地限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含 API 路由
app.include_router(users_router)
# 注册路由
app.include_router(dashscope_router)

app.include_router(ai_chat_router)

app.include_router(rag_router)

app.include_router(chroma_router)

app.include_router(employee_router)

app.include_router(chat_v2_router)

app.include_router(chat_conversations_router)

app.include_router(chat_message_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to My FastAPI Project!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
