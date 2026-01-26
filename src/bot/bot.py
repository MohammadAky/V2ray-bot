"""
Telegram bot initialization and setup
"""
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from config.settings import BOT_TOKEN
from .handlers.start import start_command
from .handlers.account import (
    add_account_command,
    delete_account_command,
    list_accounts_command
)
from .handlers.callbacks import button_callback


class V2RayBot:
    """Main bot class"""
    
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup command and callback handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("add", add_account_command))
        self.application.add_handler(CommandHandler("delete", delete_account_command))
        self.application.add_handler(CommandHandler("list", list_accounts_command))
        
        # Callback handlers
        self.application.add_handler(CallbackQueryHandler(button_callback))
    
    def run(self):
        """Start the bot"""
        print("🚀 V2Ray Bot is starting...")
        print("✅ Bot is running and ready to receive commands")
        self.application.run_polling()