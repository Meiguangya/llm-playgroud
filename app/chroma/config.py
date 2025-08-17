import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件


class Settings:
    # Chroma 配置
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "default_collection")

    # 嵌入模型配置
    # EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    # 是否启用持久化
    CHROMA_PERSIST = os.getenv("CHROMA_PERSIST", "true").lower() == "true"


settings = Settings()