
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ai.rag.loader.load_to_chroma import LoadToChroma
from app.chroma.chroma_client import ChromaSingleton


def load_pdf(file_path: Path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # print(f"{pages[0].metadata}\n")
    # print(pages[0].page_content)
    # print(f"✅ 已加载 {len(pages)} 页")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=100)
    all_splits = text_splitter.split_documents(pages)

    # 添加一些额外的操作
    total_documents = len(all_splits)
    third = total_documents // 3

    for i, document in enumerate(all_splits):
        if i < third:
            document.metadata["section"] = "beginning"
        elif i < 2 * third:
            document.metadata["section"] = "middle"
        else:
            document.metadata["section"] = "end"


    load_to_chroma = LoadToChroma(all_splits, file_path.name, ChromaSingleton.get_vectorstore())

    load_to_chroma.add_document_to_chroma()
