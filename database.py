import ollama
from pymongo import MongoClient

# Подключение к локальному серверу MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Создание базы данных
db = client["knowledge_base"]

# Создание коллекции для документов
documents_collection = db["documents"]

def save_document(text, metadata=None):
    """Сохраняет документ в MongoDB."""
    document = {
        "text": text,
        "metadata": metadata or {}
    }
    result = documents_collection.insert_one(document)
    return result.inserted_id

doc_id = save_document("Это тестовый документ", {"source": "user_upload"})
print(f"Документ сохранён с ID: {doc_id}")

def get_relevant_documents(query, limit=3):
    """Извлекает релевантные документы из MongoDB."""
    results = documents_collection.find({}, {"text": 1}).limit(limit)
    return [doc["text"] for doc in results]


def query_knowledge_base(query):
    """Запрашивает базу знаний (MongoDB) и использует Ollama для генерации ответа."""

    # Получаем релевантные документы
    documents = get_relevant_documents(query, limit=3)

    if not documents:
        return "Не найдено релевантных документов."

    # Объединяем контекст для модели
    context = " ".join(documents)

    # Создаём промпт
    prompt = f"""Ты — интеллектуальная база знаний. 
Ответь на вопрос, используя только следующий контекст:
{context}
Вопрос: {query}
Ответ:
"""
    # Отправляем запрос в Ollama
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]
