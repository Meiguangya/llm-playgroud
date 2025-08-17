from fastapi import APIRouter, Depends, HTTPException
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from app.dependencies import get_chroma_vectorstore

router = APIRouter()


@router.post("/add-texts")
async def add_texts(
        texts: list[str],
        metadatas: list[dict] = None,
        vectorstore: Chroma = Depends(get_chroma_vectorstore)
):
    """添加文本到 Chroma 集合"""
    try:
        # 确保元数据列表长度与文本列表一致
        if metadatas is None:
            metadatas = [{} for _ in texts]
        elif len(metadatas) != len(texts):
            raise ValueError("metadatas must be same length as texts")

        # 添加文本
        ids = vectorstore.add_texts(texts=texts, metadatas=metadatas)
        return {"message": "Texts added successfully", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def similarity_search(
        query: str,
        k: int = 5,
        vectorstore: Chroma = Depends(get_chroma_vectorstore)
):
    """相似性搜索"""
    try:
        results = vectorstore.similarity_search(query=query, k=k)
        return {
            "query": query,
            "results": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    # 可以添加距离分数等更多信息
                } for doc in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collection-info")
async def get_collection_info(
        vectorstore: Chroma = Depends(get_chroma_vectorstore)
):
    """获取集合信息"""
    try:
        collection = vectorstore._collection
        count = collection.count()
        metadata = collection.metadata
        return {
            "collection_name": collection.name,
            "document_count": count,
            "metadata": metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))