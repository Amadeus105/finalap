import streamlit as st
import asyncio
import bcrypt
import ollama
import telegram
import threading
from pymongo import MongoClient
from processing import process_and_store
from retrieval import query_knowledge_base
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 📌 Telegram Token
TELEGRAM_BOT_TOKEN = "7686007781:AAFVtkP5CaTFWN-soKmVO1Ihx6KiHq4VSrc"

# 📌 MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "knowledge_base"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ✅ Аутентификация
def authenticate_user(username, password):
    """Проверяет логин/пароль пользователя."""
    user = db.users.find_one({"username": username})
    return user if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]) else None

# ✅ Функция отправки сообщений в Telegram
async def send_telegram_message(chat_id, message):
    """Отправляет сообщение в Telegram."""
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message)

# ✅ Обработчик команды /start
async def start(update, context):
    await update.message.reply_text(
        "Привет! Я AI-бот знаний. Используйте /query <вопрос>, чтобы получить ответ."
    )

# ✅ Обработчик команды /query <вопрос>
async def query_telegram(update, context):
    if not context.args:
        await update.message.reply_text("⚠️ Введите запрос после /query.")
        return

    query = " ".join(context.args)
    response = query_knowledge_base(query)  # 📌 Используем твою функцию
    await update.message.reply_text(f"💡 Ответ: {response}")

# ✅ Настройка и запуск бота
async def run_telegram_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("query", query_telegram))

    print("🚀 Telegram Bot запущен!")
    await app.run_polling()

# 🔥 Запускаем Telegram-бот в фоновом потоке
def start_telegram_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_telegram_bot())

threading.Thread(target=start_telegram_thread, daemon=True).start()

# --- Streamlit UI ---
st.set_page_config(page_title="AI Knowledge Base", layout="wide")
st.title("📚 AI Knowledge Base")

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in_user = user
            st.success(f"Logged in as {username}!")
        else:
            st.error("Invalid credentials")
else:
    st.write(f"Logged in as: {st.session_state.logged_in_user['username']}")
    if st.button("Logout"):
        st.session_state.logged_in_user = None

if st.session_state.logged_in_user:
    uploaded_file = st.file_uploader("📤 Загрузите PDF", type=["pdf"])
    if uploaded_file:
        filepath = f"data/{uploaded_file.name}"
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        process_and_store(filepath)
        st.success("Документ загружен и обработан!")

    query = st.text_input("🔍 Введите ваш запрос")
    if query:
        response = query_knowledge_base(query)
        st.write("💡 Ответ:", response)

        # 🔹 Отправляем результат в Telegram (по желанию)
        chat_id = "1354210719"  # Заменить на ID пользователя или группы
        asyncio.run(send_telegram_message(chat_id, f"🔍 Запрос: {query}\n💡 Ответ: {response}"))
