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

# Xray Server Settings
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "your-server-ip")  # Use IP instead
SERVER_PORT = int(os.getenv("SERVER_PORT", "443"))  # Use port 443

# Paths
XRAY_CONFIG_PATH = os.getenv("XRAY_CONFIG_PATH", str(BASE_DIR / "config.json"))
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "xray_accounts.db"))

# Certificate paths for Reality/TLS
CERT_FILE = os.getenv("CERT_FILE", "/etc/ssl/certs/cert.crt")
KEY_FILE = os.getenv("KEY_FILE", "/etc/ssl/private/cert.key")

# Reality specific settings
REALITY_PRIVATE_KEY = os.getenv("REALITY_PRIVATE_KEY", "")
REALITY_PUBLIC_KEY = os.getenv("REALITY_PUBLIC_KEY", "")
REALITY_SHORT_ID = os.getenv("REALITY_SHORT_ID", "")
REALITY_SERVER_NAMES = os.getenv("REALITY_SERVER_NAMES", "www.google.com,www.microsoft.com").split(",")

# Xray binary path
XRAY_BINARY = os.getenv("XRAY_BINARY", "/usr/local/bin/xray")

# Ensure data directory exists
Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)

def validate_config():
    """Validate required configuration"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is required in .env file")
    if not ADMIN_IDS:
        raise ValueError("ADMIN_IDS is required in .env file")
    return True