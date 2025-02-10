import ollama
from chromadb import PersistentClient

VECTOR_DB_PATH = "vector_db/"

client = PersistentClient(path=VECTOR_DB_PATH)
collection = client.get_or_create_collection("knowledge_base")


def query_knowledge_base(query):
    """Запрашивает базу знаний и использует Ollama для генерации ответа."""
    results = collection.query(query_texts=[query], n_results=3)

    if "documents" not in results or not results["documents"]:
        return "Не найдено релевантных документов."

    context = " ".join(doc for doc_list in results["documents"] for doc in doc_list)

    prompt = f"Ты — база знаний. Ответь на вопрос, используя только контекст: {context}\nВопрос: {query}\nОтвет:"
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]
