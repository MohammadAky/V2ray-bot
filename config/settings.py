"""
Configuration settings loaded from environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Telegram Bot Settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# V2Ray Server Settings
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "your-domain.com")
SERVER_PORT = int(os.getenv("SERVER_PORT", "443"))

# Paths
V2RAY_CONFIG_PATH = os.getenv("V2RAY_CONFIG_PATH", str(BASE_DIR / "config.json"))
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "v2ray_accounts.db"))

# Certificate paths
CERT_FILE = os.getenv("CERT_FILE", "/path/to/cert.crt")
KEY_FILE = os.getenv("KEY_FILE", "/path/to/cert.key")

# Ensure data directory exists
Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)

def validate_config():
    """Validate required configuration"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is required in .env file")
    if not ADMIN_IDS:
        raise ValueError("ADMIN_IDS is required in .env file")
    return True