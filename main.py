import os
import html
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

# 🔐 ENV TOKEN
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ BOT_TOKEN not set")
    exit(1)

# 📋 Utility: Format ID with code block for easy copying
def format_id(label: str, value) -> str:
    return f"{label}\n<code>{value}</code>"

# 📋 Utility: Create copy buttons
def get_copy_keyboard(user_id: int, username: str = None, chat_id: int = None):
    buttons = []
    
    if user_id:
        buttons.append([InlineKeyboardButton("📋 Copy User ID", callback_data=f"copy_uid_{user_id}")])
    
    if chat_id:
        buttons.append([InlineKeyboardButton("📋 Copy Chat ID", callback_data=f"copy_cid_{chat_id}")])
    
    if username:
        buttons.append([InlineKeyboardButton("📋 Copy Username", callback_data=f"copy_uname_{username}")])
    
    if buttons:
        return InlineKeyboardMarkup(buttons)
    return None

# 🪪 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    
    text = f"""<b>Hi {u.first_name}! 👋</b>

I'm an info extraction bot. Here's what I can do:

<b>Your Profile</b>
<code>User ID:</code> <code>{u.id}</code>
<code>Name:</code> <code>{u.first_name} {u.last_name or ""}</code>
<code>Username:</code> <code>@{u.username if u.username else "—"}</code>
<code>Language:</code> <code>{u.language_code or "Unknown"}</code>

<b>How to Use</b>
• <b>Forward a message</b> → Get the sender's ID
• <b>Share a contact</b> → Extract contact details
• <b>Send any message</b> → Get your ID & chat info
• <b>/info</b> → Full detailed breakdown

<b>Features</b>
✨ One-tap ID copying
✨ Automatic sender detection
✨ Contact extraction
✨ Channel forwarding detection
"""
    
    keyboard = get_copy_keyboard(u.id, u.username)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

# ℹ️ /info command - Detailed info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    chat = update.effective_chat
    
    # User flags
    flags = []
    if u.is_bot:
        flags.append("🤖")
    if u.is_premium:
        flags.append("⭐")
    if not u.is_active:
        flags.append("⏸")
    
    flags_text = " ".join(flags) if flags else "—"
    
    text = f"""<b>User Details</b>

<code>ID:</code> <code>{u.id}</code>
<code>Name:</code> <code>{u.first_name} {u.last_name or ""}</code>
<code>Username:</code> <code>@{u.username if u.username else "—"}</code>
<code>Language:</code> <code>{u.language_code or "Unknown"}</code>
<code>Status:</code> <code>{flags_text}</code>

<b>Chat Details</b>

<code>Chat ID:</code> <code>{chat.id}</code>
<code>Type:</code> <code>{chat.type}</code>
<code>Name:</code> <code>{chat.title or "—"}</code>

<b>Timestamp</b>
<code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</code>
"""
    
    keyboard = get_copy_keyboard(u.id, u.username, chat.id)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

# 📞 /contact command - Show how to extract contact info
async def contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """<b>Extract Contact Info</b>

<b>How to use:</b>
1. Open your Telegram contacts
2. Select a contact
3. Tap "Share" and select this bot
4. I'll extract all details for you

<b>You'll get:</b>
✓ Contact User ID
✓ Full name
✓ Phone number
✓ All info in copyable format
"""
    
    await update.message.reply_text(text, parse_mode="HTML")

# 🧠 Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    u = msg.from_user
    chat = msg.chat
    
    if not msg:
        return
    
    try:
        # 👤 Forwarded from user
        if msg.forward_from:
            forwarded_user = msg.forward_from
            text = f"""<b>Forwarded Message</b>

<b>Original Sender</b>
<code>ID:</code> <code>{forwarded_user.id}</code>
<code>Name:</code> <code>{forwarded_user.first_name} {forwarded_user.last_name or ""}</code>
<code>Username:</code> <code>@{forwarded_user.username if forwarded_user.username else "—"}</code>

<b>Forwarded At</b>
<code>{msg.forward_date.strftime('%Y-%m-%d %H:%M:%S UTC') if msg.forward_date else 'Unknown'}</code>
"""
            keyboard = get_copy_keyboard(forwarded_user.id, forwarded_user.username)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
        
        # 📢 Forwarded from channel
        elif msg.forward_from_chat:
            channel = msg.forward_from_chat
            text = f"""<b>Channel Forward</b>

<b>Channel Details</b>
<code>ID:</code> <code>{channel.id}</code>
<code>Name:</code> <code>{channel.title or "—"}</code>
<code>Username:</code> <code>@{channel.username if channel.username else "—"}</code>
<code>Type:</code> <code>{channel.type}</code>

<b>Original Message</b>
<code>Message ID:</code> <code>{msg.forward_from_message_id or 'N/A'}</code>
"""
            keyboard = get_copy_keyboard(None, channel.username, channel.id)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
        
        # 📞 Contact shared
        elif msg.contact:
            contact = msg.contact
            text = f"""<b>Contact Details</b>

<b>Contact Info</b>
<code>Phone:</code> <code>{contact.phone_number}</code>
<code>Name:</code> <code>{contact.first_name} {contact.last_name or ""}</code>
<code>User ID:</code> <code>{contact.user_id or "Not linked"}</code>

<b>Shared By</b>
<code>Your ID:</code> <code>{u.id}</code>
<code>Chat ID:</code> <code>{chat.id}</code>
"""
            keyboard = get_copy_keyboard(contact.user_id or u.id, None, chat.id)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
        
        # 🆔 Regular message
        else:
            text = f"""<b>Your Information</b>

<b>Sender</b>
<code>ID:</code> <code>{u.id}</code>
<code>Name:</code> <code>{u.first_name} {u.last_name or ""}</code>
<code>Username:</code> <code>@{u.username if u.username else "—"}</code>

<b>Chat</b>
<code>ID:</code> <code>{chat.id}</code>
<code>Type:</code> <code>{chat.type}</code>

<b>Message</b>
<code>ID:</code> <code>{msg.message_id}</code>
"""
            keyboard = get_copy_keyboard(u.id, u.username, chat.id)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    except Exception as e:
        await msg.reply_text(f"<b>Error</b>\n<code>{html.escape(str(e))}</code>", parse_mode="HTML")

# 📋 Callback handler for copy buttons
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("copy_uid_"):
        uid = data.split("_")[-1]
        text = f"✅ User ID copied!\n\n<code>{uid}</code>"
    elif data.startswith("copy_cid_"):
        cid = data.split("_")[-1]
        text = f"✅ Chat ID copied!\n\n<code>{cid}</code>"
    elif data.startswith("copy_uname_"):
        uname = data.split("_", 2)[-1]
        text = f"✅ Username copied!\n\n<code>@{uname}</code>"
    else:
        text = "❓ Unknown action"
    
    await query.edit_message_text(text, parse_mode="HTML")

async def main():
    """Main async entry point for the bot"""
    app = Application.builder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("contact", contact_info))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    
    print("🚀 Advanced Info Bot initializing...")
    print("📋 Features: /start, /info, /contact")
    
    # Initialize and start the bot
    async with app:
        await app.initialize()
        await app.start()
        print("✅ Bot started successfully!")
        print("🔄 Running in polling mode...")
        
        try:
            await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        except KeyboardInterrupt:
            print("🛑 Received interrupt signal")
        finally:
            await app.stop()
            await app.shutdown()
            print("🛑 Bot stopped cleanly")

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot terminated by user")
