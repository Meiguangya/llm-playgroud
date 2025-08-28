from app.chroma.chroma_client import ChromaSingleton
from langchain.tools.retriever import create_retriever_tool

chroma_retriever = ChromaSingleton.get_vectorstore().as_retriever()


retrieve_desc = """
从本地知识库中检索与用户问题相关的文档片段。
适用场景：
- 公司政策（如“年假怎么休”）
- 产品使用说明
- 人物简介
不适用于实时信息（如天气、股价）或计算、数据库查询等。
"""

retriever_tool = create_retriever_tool(
    chroma_retriever,
    "retrieve_document",
    retrieve_desc,
)