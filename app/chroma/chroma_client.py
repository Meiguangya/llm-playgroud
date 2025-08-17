from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

from app.chroma.config import settings
from app.embedding.embedding_model import  EmbeddingFactory

class ChromaSingleton:
    _instance = None
    _vectorstore = None
    _embedding_function = None

    @classmethod
    def get_embedding_function(cls):
        """获取单例嵌入函数"""
        if cls._embedding_function is None:
            cls._embedding_function = EmbeddingFactory.get_dashscope_embedding()
        return cls._embedding_function

    @classmethod
    def get_vectorstore(cls):
        """获取单例 Chroma 向量存储"""
        if cls._vectorstore is None:
            embedding_function = cls.get_embedding_function()

            # 创建或加载向量存储
            cls._vectorstore = Chroma(
                collection_name=settings.CHROMA_COLLECTION_NAME,
                embedding_function=embedding_function,
                persist_directory=settings.CHROMA_PERSIST_DIR if settings.CHROMA_PERSIST else None
            )

            # 确保集合存在
            try:
                coll = cls._vectorstore._collection.get()
                print(f"collection get 成功{coll}")
            except:
                # 如果集合不存在则创建空集合
                cls._vectorstore.add_texts(texts=["Initial document"], metadatas=[{}])


        return cls._vectorstore

    @classmethod
    def reset(cls):
        """重置实例（主要用于测试）"""
        cls._instance = None
        cls._vectorstore = None
        cls._embedding_function = None