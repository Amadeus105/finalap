import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb import PersistentClient

VECTOR_DB_PATH = "vector_db/"

def load_document(filepath):
    """Загружает PDF и разбивает на части."""
    loader = PyPDFLoader(filepath)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(pages)

def store_in_chromadb(docs):
    """Сохраняет документы в ChromaDB."""
    client = PersistentClient(path=VECTOR_DB_PATH)
    collection = client.get_or_create_collection("knowledge_base")
    for i, doc in enumerate(docs):
        collection.add(
            documents=[doc.page_content],
            metadatas=[{"source": doc.metadata["source"]}],
            ids=[str(i)]
        )

def process_and_store(filepath):
    """Основной процесс загрузки и сохранения документа."""
    docs = load_document(filepath)
    store_in_chromadb(docs)
