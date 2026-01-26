"""
Start command handler
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config.settings import ADMIN_IDS


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Unauthorized access")
        return
    
    keyboard = [
        [InlineKeyboardButton("➕ Add Account", callback_data="add")],
        [InlineKeyboardButton("📋 List Accounts", callback_data="list")],
        [InlineKeyboardButton("🗑 Delete Account", callback_data="delete")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🎛 *V2Ray Admin Panel*\n\n"
        "Welcome to your V2Ray management bot!\n"
        "Select an option below to get started."
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )