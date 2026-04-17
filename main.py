import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ BOT_TOKEN not set")
    exit(1)

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

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🚀 Bot running...")

    # stable polling
    app.run_polling()

if __name__ == "__main__":
    main()
