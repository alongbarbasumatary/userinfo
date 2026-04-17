import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN not set in environment")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    text = f"""
🤖 Info Bot

🆔 ID: {u.id}
👤 Name: {u.first_name}
🔗 Username: @{u.username if u.username else "None"}
🌐 Language: {u.language_code}

📌 Forward message → get sender ID
📞 Send contact → get contact ID
"""

    await update.message.reply_text(text)

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    # Forwarded user
    if msg.forward_from:
        u = msg.forward_from
        await msg.reply_text(f"🆔 Sender ID: {u.id}\n👤 {u.first_name}")

    # Forwarded channel
    elif msg.forward_from_chat:
        c = msg.forward_from_chat
        await msg.reply_text(f"📢 Channel ID: {c.id}")

    # Contact
    elif msg.contact:
        await msg.reply_text(f"📞 Contact ID: {msg.contact.user_id}")

    # Normal message
    else:
        u = msg.from_user
        await msg.reply_text(f"🆔 Your ID: {u.id}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handler))

    app.run_polling()

if __name__ == "__main__":
    main()
