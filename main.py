import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 ENV TOKEN
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ BOT_TOKEN not set")
    exit(1)

# 🪪 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    await update.message.reply_text(
        f"""
🤖 Info Bot

🪪 Your Telegram Info

🆔 ID: {u.id}
👤 Name: {u.first_name}
🔗 Username: @{u.username if u.username else "None"}
🌐 Language: {u.language_code}

📌 Forward message → sender ID
📞 Send contact → contact ID
"""
    )

# 🧠 message handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg:
        return

    try:
        # 👤 forwarded user
        if msg.forward_from:
            await msg.reply_text(f"🆔 Sender ID: {msg.forward_from.id}")

        # 📢 channel forward
        elif msg.forward_from_chat:
            await msg.reply_text(f"📢 Channel ID: {msg.forward_from_chat.id}")

        # 📞 contact
        elif msg.contact:
            await msg.reply_text(f"📞 Contact ID: {msg.contact.user_id}")

        # 🆔 normal
        else:
            await msg.reply_text(f"🆔 Your ID: {msg.from_user.id}")

    except Exception:
        await msg.reply_text("⚠️ Error processing message")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle))

    print("🚀 Bot running...")

    # 🔥 FIX Render asyncio crash
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
