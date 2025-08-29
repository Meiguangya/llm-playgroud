from fastapi import Depends
from app.chroma.chroma_client import ChromaSingleton
from langchain_community.vectorstores import Chroma

def get_chroma_vectorstore() -> Chroma:
    """获取 Chroma 向量存储的依赖项"""
    return ChromaSingleton.get_vectorstore()