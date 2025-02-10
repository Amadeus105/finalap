# AI Knowledge Base with Telegram Bot

## 📌 Project Overview
This project is an AI-powered knowledge base that allows users to upload and search documents using a web interface built with Streamlit. Additionally, it includes a Telegram bot for interacting with the knowledge base directly from Telegram.

## 🚀 Features
- User authentication with MongoDB
- Upload and process PDF/TXT documents
- Store processed data in a knowledge base
- Query the knowledge base using AI
- Telegram bot integration for remote access

---

## 📂 Installation
### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/ai-knowledge-base.git
cd ai-knowledge-base
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate  # On Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration
### 1️⃣ Set up MongoDB
Make sure you have MongoDB installed and running. Update the `MONGO_URI` in `config.py` if necessary:
```python
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "knowledge_base"
```

### 2️⃣ Configure Telegram Bot
1. Create a bot using [@BotFather](https://t.me/BotFather) on Telegram.
2. Get the bot token and update `config.py`:
```python
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
```

---

## ▶️ Running the Application
### 1️⃣ Start MongoDB
Ensure MongoDB is running before launching the app.

### 2️⃣ Run the Streamlit Web App
```bash
streamlit run app.py
```

### 3️⃣ Run the Telegram Bot
```bash
python telegram_bot.py
```

---

## 📌 Usage Guide
### Web App
1. Open the Streamlit interface.
2. Log in or create an account.
3. Upload PDF or TXT files.
4. Enter search queries to find relevant documents.

### Telegram Bot
Use the following commands:
- `/start` – Start the bot
- `/addfile` – Upload a document
- `/open` – List all documents
- `/search <keywords>` – Search for documents
- `/help` – Show available commands

---

## 🔧 Troubleshooting
### `RuntimeError: Cannot run the event loop while another loop is running`
- Use `asyncio.run()` only in standalone scripts, not inside Streamlit.
- Modify `telegram_bot.py` to:
  ```python
  import asyncio
  from telegram.ext import Application
  
  async def main():
      app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
      await app.run_polling()
  
  if __name__ == "__main__":
      asyncio.run(main())
  ```

### Connection Issues
- Ensure MongoDB is running.
- Check if the Telegram bot token is correct.

---

## 📜 License
Project made by Shaikenov Aidyn,Khunakhan Astana,Abduali Aisultan.

---

## 💡 Contributing
Pull requests are welcome! Feel free to open an issue for bug reports or feature requests.

