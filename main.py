import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8080))

if not TOKEN:
    print("❌ BOT_TOKEN not set")
    exit(1)

# ---------- Telegram Bot ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    await update.message.reply_text(
        f"""
🤖 Info Bot

🪪 Telegram User Info

🆔 ID: {u.id}
👤 Name: {u.first_name}
🔗 Username: @{u.username if u.username else "None"}
🌐 Language: {u.language_code}
"""
    )

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 Bot running...")
    app.run_polling()

# ---------- Web Server (PORT 8080) ----------
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running 🚀"

if __name__ == "__main__":
    # run bot in background
    threading.Thread(target=run_bot).start()

    # open port 8080 for Render
    web.run(host="0.0.0.0", port=PORT)
