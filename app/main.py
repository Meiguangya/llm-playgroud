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
from app.api.rag import  router as rag_router
from app.chroma.chroma_client import ChromaSingleton
from app.api.chroma_router import router as chroma_router
from app.ai.rag.loader.load_system_file import LoadSystemFile

from app.api.employee import router as employee_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时初始化 Chroma 客户端
    print("Initializing Chroma client...")
    ChromaSingleton.get_vectorstore()  # 触发初始化
    logger.info("Chroma 客户端初始化成功")

    print("将数据加载到chroma中")

    # 加个配置
    # LoadSystemFile.load_system_file()

    yield
    logger.info("应用关闭中...")


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
app.include_router(users_router, prefix="/api/v1", tags=["users"])
# 注册路由
app.include_router(dashscope_router)

app.include_router(ai_chat_router)

app.include_router(rag_router)

app.include_router(chroma_router, prefix="/api/v1/chroma",tags=["chroma"])

app.include_router(employee_router,tags=["employees"])


@app.get("/")
def read_root():
    return {"message": "Welcome to My FastAPI Project!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}