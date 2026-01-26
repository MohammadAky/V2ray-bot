"""
Callback query handlers for inline buttons
"""
from telegram import Update
from telegram.ext import ContextTypes

from src.database.db import Database
from src.utils.helpers import format_bytes, format_date, get_status_emoji
from config.settings import DATABASE_PATH

db = Database(DATABASE_PATH)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "add":
        text = (
            "➕ *Add New Account*\n\n"
            "Use one of these commands:\n\n"
            "*For data limit:*\n"
            "`/add email@example.com data 10`\n"
            "_(10 GB limit)_\n\n"
            "*For time limit:*\n"
            "`/add email@example.com time 30`\n"
            "_(30 days)_"
        )
        await query.message.reply_text(text, parse_mode="Markdown")
    
    elif query.data == "list":
        accounts = db.list_accounts()
        
        if not accounts:
            await query.message.reply_text("📋 No accounts found")
            return
        
        text = "📋 *All Accounts*\n\n"
        
        for acc in accounts:
            status_emoji = get_status_emoji(acc.status)
            text += f"{status_emoji} `{acc.email}`\n"
            
            if acc.limit_type == "data":
                remaining = acc.get_remaining_data()
                text += f"   📊 {remaining:.2f} GB / {acc.data_limit} GB\n"
            else:
                remaining = acc.get_remaining_days()
                text += f"   ⏰ {remaining} days left\n"
            
            text += f"   📈 {format_bytes(acc.total_traffic)}\n\n"
        
        await query.message.reply_text(text, parse_mode="Markdown")
    
    elif query.data == "delete":
        text = (
            "🗑 *Delete Account*\n\n"
            "Use command:\n"
            "`/delete email@example.com`"
        )
        await query.message.reply_text(text, parse_mode="Markdown")
    
    elif query.data == "help":
        text = (
            "ℹ️ *Bot Commands*\n\n"
            "`/start` - Show main menu\n"
            "`/add` - Add new account\n"
            "`/delete` - Delete account\n"
            "`/list` - List all accounts\n\n"
            "*Examples:*\n"
            "`/add user@test.com data 50`\n"
            "`/add user@test.com time 30`\n"
            "`/delete user@test.com`"
        )
        await query.message.reply_text(text, parse_mode="Markdown")