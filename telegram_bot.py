import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from app import add_document_to_chromadb, extract_text_from_pdf, extract_text_from_txt, list_documents, retrieve_documents_by_keywords

# 🔹 Твой токен бота
TELEGRAM_BOT_TOKEN = "7686007781:AAFVtkP5CaTFWN-soKmVO1Ihx6KiHq4VSrc"

# ✅ Функция для отправки сообщений в Telegram
async def send_telegram_message(chat_id, message):
    """Отправляет сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

# ✅ Команда /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Я AI-бот.\n"
        "Отправьте документ (PDF/TXT) с командой /addfile.\n"
        "Введите /open, чтобы посмотреть список документов.\n"
        "Используйте /search <ключевые слова> для поиска."
    )

# ✅ Команда /open (Список документов)
async def open_documents(update: Update, context: CallbackContext):
    docs = list_documents()
    doc_list = "\n".join(docs)

    # ✅ Отправляем текст частями, если он слишком длинный
    await send_long_message(update, f"📂 Список документов:\n{doc_list}")


# ✅ Команда /help (Список команд)
# ✅ Команда /help (Список команд с описанием)
async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "📌 **Список доступных команд:**\n\n"
        "🔹 `/start` – Начать работу, показать приветственное сообщение\n"
        "🔹 `/open` – Посмотреть список всех добавленных документов\n"
        "🔹 `/search <ключевые слова>` – Найти документ по ключевым словам\n"
        "🔹 `/addfile` – Отправить PDF/TXT файл и добавить его в базу\n"
        "🔹 `/help` – Показать список команд с описанием\n"
    )

    await update.message.reply_text(help_text, parse_mode="Markdown")

# ✅ Команда /search (Поиск по ключевым словам)
async def search_documents(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("⚠️ Введите ключевые слова после команды /search.")
        return

    results = retrieve_documents_by_keywords(query)

    if not results or results == ["Документы не найдены."]:
        await update.message.reply_text("⚠️ Ничего не найдено!")
        return

    doc_list = "\n".join([" ".join(map(str, doc)) for doc in results])

    # ✅ Отправляем текст частями, если он слишком длинный
    await send_long_message(update, f"🔍 Найденные документы:\n{doc_list}")


    # ✅ Преобразуем список списков в текст
    doc_list = "\n".join([" ".join(map(str, doc)) for doc in results])

    await update.message.reply_text(f"🔍 Найденные документы:\n{doc_list}")

# ✅ Функция для обработки документов (PDF, TXT)
async def handle_document(update: Update, context: CallbackContext):
    document = update.message.document
    chat_id = update.message.chat_id
    file_id = document.file_id
    file_name = document.file_name
    file_extension = file_name.split(".")[-1].lower()

    if file_extension not in ["pdf", "txt"]:
        await update.message.reply_text("⚠️ Поддерживаются только файлы PDF и TXT.")
        return

    file = await context.bot.get_file(file_id)
    file_path = f"downloads/{file_name}"
    
    os.makedirs("downloads", exist_ok=True)

    await file.download_to_drive(file_path)
    
    if file_extension == "pdf":
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_txt(file_path)

    add_document_to_chromadb(text, f"Пользователь {chat_id}", "telegram")

    await update.message.reply_text(f"📂 Документ '{file_name}' добавлен в базу!")

# ✅ Функция разбиения длинных сообщений
async def send_long_message(update, text, chunk_size=4000):
    """Отправляет сообщение частями, если оно слишком длинное"""
    for i in range(0, len(text), chunk_size):
        await update.message.reply_text(text[i:i+chunk_size])

# 🔹 Запуск бота
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # ✅ Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("open", open_documents))  # ✅ Теперь команда работает
    app.add_handler(CommandHandler("help", help_command))  # ✅ Теперь команда работает
    app.add_handler(CommandHandler("search", search_documents))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🚀 Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()

