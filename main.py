import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN:
    print("BOT_TOKEN missing")
    exit(1)

# ---------- Telegram Bot ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    text = f"""🤖 Info Bot

🪪 Telegram User Info

🆔 ID: {u.id}
👤 Name: {u.first_name}
🔗 Username: @{u.username if u.username else "None"}
🌐 Language: {u.language_code}
"""

    await update.message.reply_text(text)

# ---------- Web Server ----------
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running 🚀"

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # start bot WITHOUT blocking Flask
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    import threading

    threading.Thread(target=main).start()

    web.run(host="0.0.0.0", port=PORT)
