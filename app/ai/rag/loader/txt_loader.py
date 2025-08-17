from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.chroma.chroma_client import ChromaSingleton
from app.ai.rag.loader.load_to_chroma import LoadToChroma


def load_txt(file_path: Path):
    print(f"📄 正在处理 TXT 文件: {file_path.name}")

    loader = TextLoader(file_path, encoding="utf-8")

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)

    all_splits = text_splitter.split_documents(docs)

    load_to_chroma = LoadToChroma(all_splits, file_path.name, ChromaSingleton.get_vectorstore())

    load_to_chroma.add_document_to_chroma()

    return {
        "type": "txt",
        "filename": file_path.name,
        "result": "success"
    }
