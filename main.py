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
    
    text = f"""
╔═══════════════════════════════╗
║  🤖 <b>Advanced Info Bot</b>     ║
╚═══════════════════════════════╝

<b>👤 Your Profile:</b>
{format_id("🆔 User ID", u.id)}
{format_id("👤 First Name", u.first_name)}
{format_id("📛 Last Name", u.last_name or "—")}
{format_id("🔗 Username", f"@{u.username}" if u.username else "—")}
{format_id("🌐 Language", u.language_code or "Unknown")}

<b>📌 Usage:</b>
• Forward a message → Get sender ID
• Send a contact → Get contact ID
• Send any message → Get your ID
• Use /info → Detailed user info

<b>✨ Features:</b>
✓ Copy IDs easily with buttons
✓ Sender identification
✓ Contact info extraction
✓ Chat & Channel detection
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
        flags.append("🤖 Bot")
    if u.is_premium:
        flags.append("⭐ Premium")
    if not u.is_active:
        flags.append("❌ Inactive")
    
    flags_text = " | ".join(flags) if flags else "None"
    
    text = f"""
╔═══════════════════════════════╗
║  📊 <b>Detailed User Info</b>    ║
╚═══════════════════════════════╝

<b>👤 User Details:</b>
{format_id("🆔 User ID", u.id)}
{format_id("👤 First Name", u.first_name)}
{format_id("📛 Last Name", u.last_name or "—")}
{format_id("🔗 Username", f"@{u.username}" if u.username else "—")}
{format_id("🌐 Language Code", u.language_code or "Unknown")}

<b>🚩 Flags:</b>
<code>{flags_text}</code>

<b>💬 Chat Details:</b>
{format_id("💬 Chat ID", chat.id)}
{format_id("💬 Chat Type", chat.type)}
{format_id("💬 Chat Title", chat.title or "—")}

<b>🕐 Timestamp:</b>
<code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</code>
"""
    
    keyboard = get_copy_keyboard(u.id, u.username, chat.id)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

# 📞 /contact command - Show how to extract contact info
async def contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
╔═══════════════════════════════╗
║  📞 <b>Contact Info Guide</b>   ║
╚═══════════════════════════════╝

<b>📱 How to use:</b>
1. Open your contacts
2. Select a contact
3. Share it with this bot
4. Bot will show you contact details

<b>ℹ️ What you'll get:</b>
✓ Contact User ID
✓ Contact Name
✓ Contact Phone Number
✓ Copy-ready format
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
            text = f"""
╔═══════════════════════════════╗
║  👤 <b>Forwarded Message</b>    ║
╚═══════════════════════════════╝

<b>📤 Original Sender:</b>
{format_id("🆔 User ID", forwarded_user.id)}
{format_id("👤 First Name", forwarded_user.first_name)}
{format_id("📛 Last Name", forwarded_user.last_name or "—")}
{format_id("🔗 Username", f"@{forwarded_user.username}" if forwarded_user.username else "—")}

<b>🕐 Forwarded At:</b>
<code>{msg.forward_date.strftime('%Y-%m-%d %H:%M:%S UTC') if msg.forward_date else 'Unknown'}</code>
"""
            keyboard = get_copy_keyboard(forwarded_user.id, forwarded_user.username)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
        
        # 📢 Forwarded from channel
        elif msg.forward_from_chat:
            channel = msg.forward_from_chat
            text = f"""
╔═══════════════════════════════╗
║  📢 <b>Channel Forward</b>      ║
╚═══════════════════════════════╝

<b>📡 Channel Details:</b>
{format_id("📢 Channel ID", channel.id)}
{format_id("📛 Channel Name", channel.title or "—")}
{format_id("🔗 Channel Username", f"@{channel.username}" if channel.username else "—")}
{format_id("📊 Channel Type", channel.type)}

<b>📌 Original Message ID:</b>
<code>{msg.forward_from_message_id or 'N/A'}</code>
"""
            keyboard = get_copy_keyboard(None, channel.username, channel.id)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
        
        # 📞 Contact shared
        elif msg.contact:
            contact = msg.contact
            text = f"""
╔═══════════════════════════════╗
║  📞 <b>Contact Info</b>        ║
╚═══════════════════════════════╝

<b>👤 Contact Details:</b>
{format_id("📞 Phone", contact.phone_number)}
{format_id("👤 First Name", contact.first_name)}
{format_id("📛 Last Name", contact.last_name or "—")}
{format_id("🆔 User ID", contact.user_id or "Not linked")}

<b>📌 Shared by:</b>
{format_id("🆔 Your ID", u.id)}
{format_id("💬 Chat ID", chat.id)}
"""
            keyboard = get_copy_keyboard(contact.user_id or u.id, None, chat.id)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
        
        # 🆔 Regular message
        else:
            text = f"""
╔═══════════════════════════════╗
║  🆔 <b>Your ID</b>            ║
╚═══════════════════════════════╝

<b>👤 Sender Info:</b>
{format_id("🆔 User ID", u.id)}
{format_id("👤 First Name", u.first_name)}
{format_id("📛 Last Name", u.last_name or "—")}
{format_id("🔗 Username", f"@{u.username}" if u.username else "—")}

<b>💬 Chat Info:</b>
{format_id("💬 Chat ID", chat.id)}
{format_id("💬 Chat Type", chat.type)}

<b>📌 Message ID:</b>
<code>{msg.message_id}</code>
"""
            keyboard = get_copy_keyboard(u.id, u.username, chat.id)
            await msg.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    except Exception as e:
        await msg.reply_text(f"⚠️ Error: <code>{html.escape(str(e))}</code>", parse_mode="HTML")

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

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("contact", contact_info))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    
    print("🚀 Advanced Info Bot started!")
    print("📋 Features: /start, /info, /contact")
    
    app.run_polling()

if __name__ == "__main__":
    main()
