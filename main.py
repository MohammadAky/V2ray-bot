"""
Main entry point for V2Ray Bot
"""
from config.settings import validate_config
from src.bot.bot import V2RayBot


def main():
    """Main function"""
    try:
        # Validate configuration
        validate_config()
        
        # Initialize and run bot
        bot = V2RayBot()
        bot.run()
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please check your .env file")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()