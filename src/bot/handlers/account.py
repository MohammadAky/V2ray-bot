"""
Account management handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import ADMIN_IDS, DATABASE_PATH
from src.database.db import Database
from src.v2ray.config_manager import XrayConfigManager
from src.v2ray.client_generator import ClientConfigGenerator
from src.utils.validators import Validator
from src.utils.helpers import format_bytes, format_date, get_status_emoji

db = Database(DATABASE_PATH)
v2ray = XrayConfigManager()
client_gen = ClientConfigGenerator()


async def add_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /add command"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Unauthorized access")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ *Invalid format*\n\n"
            "Usage:\n"
            "`/add email@example.com data 10`\n"
            "`/add email@example.com time 30`",
            parse_mode="Markdown"
        )
        return
    
    email = context.args[0]
    limit_type = context.args[1].lower()
    limit_value = context.args[2]
    
    # Validate input
    if not Validator.is_valid_email(email):
        await update.message.reply_text("❌ Invalid email format")
        return
    
    if not Validator.is_valid_limit_type(limit_type):
        await update.message.reply_text("❌ Limit type must be 'data' or 'time'")
        return
    
    if not Validator.is_positive_integer(limit_value):
        await update.message.reply_text("❌ Limit value must be a positive number")
        return
    
    limit_value = int(limit_value)
    
    # Create account
    if limit_type == "data":
        account = db.create_account(email, "data", data_limit=limit_value)
    else:
        account = db.create_account(email, "time", days=limit_value)
    
    if not account:
        await update.message.reply_text("❌ Account already exists with this email")
        return
    
    # Add to V2Ray config
    v2ray.add_client(email, account.uuid)

    # Get Reality keys for client config
    reality_keys = v2ray.get_reality_keys()

    # Generate client config
    config_link = client_gen.generate_vless_link(email, account.uuid, reality_keys)
    
    response = (
        f"✅ *Account Created Successfully*\n\n"
        f"📧 Email: `{email}`\n"
        f"🆔 UUID: `{account.uuid}`\n"
        f"📊 Type: {limit_type.upper()}\n"
        f"📈 Limit: {limit_value} {'GB' if limit_type == 'data' else 'days'}\n"
        f"📅 Created: {format_date(account.created_date)}\n\n"
        f"🔗 *Config Link:*\n`{config_link}`\n\n"
        f"⚠️ *Important:* Restart V2Ray service:\n"
        f"`systemctl restart v2ray`"
    )
    
    await update.message.reply_text(response, parse_mode="Markdown")


async def delete_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /delete command"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Unauthorized access")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ Usage: `/delete email@example.com`",
            parse_mode="Markdown"
        )
        return
    
    email = context.args[0]
    
    # Check if account exists
    account = db.get_account(email)
    if not account:
        await update.message.reply_text("❌ Account not found")
        return
    
    # Delete from database and V2Ray
    db.delete_account(email)
    v2ray.remove_client(email)
    
    await update.message.reply_text(
        f"✅ *Account Deleted*\n\n"
        f"📧 Email: `{email}`\n\n"
        f"⚠️ Restart V2Ray service:\n"
        f"`systemctl restart v2ray`",
        parse_mode="Markdown"
    )


async def list_accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /list command"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Unauthorized access")
        return
    
    accounts = db.list_accounts()
    
    if not accounts:
        await update.message.reply_text("📋 No accounts found")
        return
    
    text = "📋 *Active Accounts*\n\n"
    
    for acc in accounts:
        status_emoji = get_status_emoji(acc.status)
        text += f"{status_emoji} `{acc.email}`\n"
        
        if acc.limit_type == "data":
            remaining = acc.get_remaining_data()
            text += f"   📊 Data: {remaining:.2f} GB / {acc.data_limit} GB\n"
        else:
            remaining = acc.get_remaining_days()
            text += f"   ⏰ Time: {remaining} days left\n"
        
        text += f"   📈 Used: {format_bytes(acc.total_traffic)}\n"
        text += f"   📅 Created: {format_date(acc.created_date)}\n\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")