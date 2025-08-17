import hashlib

from langchain_chroma import Chroma
from langchain_core.documents import Document


class LoadToChroma:

    def __init__(self,
                 all_splits: list[Document],
                 file_name: str,
                 vector_store: Chroma):
        self.all_splits = all_splits
        self.file_name = file_name
        self.vector_store = vector_store

    def generate_doc_id(self,
                        doc: Document):
        """使用 source URL 和内容的哈希生成唯一 ID"""
        content = doc.page_content
        hash_object = hashlib.md5((self.file_name + content).encode('utf-8')).hexdigest()
        return hash_object

    def filter_split(self):

        # 为每个 split 生成唯一 ID
        ids = [self.generate_doc_id(doc) for doc in self.all_splits]

        # 查询已存在的ids
        existing_ids = self.vector_store.get()["ids"]
        print(f"已存在 {len(existing_ids)} 个文档片段")

        # 过滤出尚未添加的文档
        new_splits = []
        new_ids = []
        for doc, doc_id in zip(self.all_splits, ids):
            if doc_id not in existing_ids:
                new_splits.append(doc)
                new_ids.append(doc_id)

        return new_splits, new_ids

    def add_document_to_chroma(self):
        new_splits, new_ids = self.filter_split()

        # 5. 只添加新文档
        if new_splits:
            print(f"新增 {len(new_splits)} 个文档片段")
            self.vector_store.add_documents(documents=new_splits, ids=new_ids)
        else:
            print("所有文档已存在，无需添加。")

        print("======加载完成====")
