import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN not set")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(
        f"🪪 Info Bot\n\n🆔 ID: {u.id}\n👤 Name: {u.first_name}\n🔗 @{u.username}"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.forward_from:
        u = msg.forward_from
        await msg.reply_text(f"🆔 Sender ID: {u.id}")

    elif msg.forward_from_chat:
        c = msg.forward_from_chat
        await msg.reply_text(f"📢 Channel ID: {c.id}")

    elif msg.contact:
        await msg.reply_text(f"📞 Contact ID: {msg.contact.user_id}")

    else:
        await msg.reply_text(f"🆔 Your ID: {msg.from_user.id}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle))

    app.run_polling()

if __name__ == "__main__":
    main()
