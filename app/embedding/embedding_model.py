
from langchain_community.embeddings import DashScopeEmbeddings
import os


class EmbeddingFactory:

    _inst_dashscope = None

    @classmethod
    def get_dashscope_embedding(cls):
        """获取embedding模型"""
        if cls._inst_dashscope is None:
            cls._inst_dashscope = DashScopeEmbeddings(
                model = "text-embedding-v3",
                dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
            )

        return cls._inst_dashscope
