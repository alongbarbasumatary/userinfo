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

    text = (
        "╔══════════════════════════════╗\n"
        "║        🤖  INFO  BOT         ║\n"
        "╚══════════════════════════════╝\n"
        "\n"
        "📋  <b>Your Telegram Info</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔  <b>ID</b>          →  <code>{u.id}</code>\n"
        f"👤  <b>First Name</b>  →  {u.first_name}\n"
        f"🔗  <b>Username</b>    →  @{u.username if u.username else 'None'}\n"
        f"🌐  <b>Language</b>    →  {u.language_code if u.language_code else 'Unknown'}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "\n"
        "📌  Forward a message  →  get sender ID\n"
        "📢  Forward from channel  →  get channel ID\n"
        "📞  Send a contact  →  get contact ID\n"
        "\n"
        "╔══════════════════════════════╗\n"
        "║  Send anything to get info!  ║\n"
        "╚══════════════════════════════╝"
    )

    await update.message.reply_text(text, parse_mode="HTML")

# 🧠 handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg:
        return

    try:
        # 👤 forwarded private user
        if msg.forward_from:
            u = msg.forward_from
            text = (
                "╔══════════════════════════════╗\n"
                "║     👤  FORWARDED  USER      ║\n"
                "╚══════════════════════════════╝\n"
                "\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔  <b>User ID</b>      →  <code>{u.id}</code>\n"
                f"👤  <b>First Name</b>  →  {u.first_name}\n"
                f"🔗  <b>Username</b>    →  @{u.username if u.username else 'None'}\n"
                f"🤖  <b>Is Bot</b>      →  {'Yes' if u.is_bot else 'No'}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
            await msg.reply_text(text, parse_mode="HTML")

        # 📢 forwarded from channel/group
        elif msg.forward_from_chat:
            c = msg.forward_from_chat
            text = (
                "╔══════════════════════════════╗\n"
                "║     📢  FORWARDED  CHAT      ║\n"
                "╚══════════════════════════════╝\n"
                "\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔  <b>Chat ID</b>     →  <code>{c.id}</code>\n"
                f"📛  <b>Title</b>       →  {c.title if c.title else 'N/A'}\n"
                f"🔗  <b>Username</b>    →  @{c.username if c.username else 'None'}\n"
                f"📂  <b>Type</b>        →  {c.type}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
            await msg.reply_text(text, parse_mode="HTML")

        # 📞 contact shared
        elif msg.contact:
            co = msg.contact
            text = (
                "╔══════════════════════════════╗\n"
                "║       📞  CONTACT  INFO      ║\n"
                "╚══════════════════════════════╝\n"
                "\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔  <b>User ID</b>     →  <code>{co.user_id if co.user_id else 'N/A'}</code>\n"
                f"👤  <b>First Name</b>  →  {co.first_name if co.first_name else 'N/A'}\n"
                f"📱  <b>Phone</b>       →  <code>{co.phone_number}</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
            await msg.reply_text(text, parse_mode="HTML")

        # 🆔 normal message — show sender info
        else:
            u = msg.from_user
            chat = msg.chat
            text = (
                "╔══════════════════════════════╗\n"
                "║       🆔  MESSAGE  INFO      ║\n"
                "╚══════════════════════════════╝\n"
                "\n"
                "👤  <b>Sender</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔  <b>Your ID</b>     →  <code>{u.id}</code>\n"
                f"👤  <b>Name</b>        →  {u.first_name}\n"
                f"🔗  <b>Username</b>    →  @{u.username if u.username else 'None'}\n"
                "\n"
                "💬  <b>Chat</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔  <b>Chat ID</b>     →  <code>{chat.id}</code>\n"
                f"📂  <b>Chat Type</b>   →  {chat.type}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
            await msg.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await msg.reply_text(
            "╔══════════════════════╗\n"
            "║   ⚠️  ERROR occurred  ║\n"
            "╚══════════════════════╝\n"
            f"\n<code>{e}</code>",
            parse_mode="HTML"
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle))

    print("🚀 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
