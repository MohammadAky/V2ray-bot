# XRay Telegram Bot

A modular Telegram bot for managing XRay VPN accounts with data and time limits.

## Features

- ✅ Add accounts with data limit (GB) or time limit (days)
- ✅ Delete accounts
- ✅ List all accounts with usage statistics
- ✅ TLS configuration support
- ✅ SQLite database
- ✅ Modular architecture
- ✅ Easy to maintain and extend

## Project Structure

```
v2ray-bot/
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
├── config/
│   └── settings.py                  # Configuration
├── src/
│   ├── bot/
│   │   ├── bot.py                  # Bot initialization
│   │   └── handlers/               # Command handlers
│   ├── database/
│   │   ├── db.py                   # Database operations
│   │   └── models.py               # Data models
│   ├── v2ray/
│   │   ├── config_manager.py       # V2Ray config
│   │   └── client_generator.py    # Client configs
│   └── utils/
│       ├── validators.py           # Validation
│       └── helpers.py              # Helpers
└── data/                            # Database files
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=your_telegram_user_id
SERVER_ADDRESS=your-domain.com
SERVER_PORT=443
```

### 3. Run the Bot

```bash
python main.py
```

## Commands

- `/start` - Show main menu
- `/add email@example.com data 10` - Add account with 10GB limit
- `/add email@example.com time 30` - Add account with 30 days
- `/delete email@example.com` - Delete account
- `/list` - List all accounts

## Getting Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow instructions
4. Copy the token

## Getting Your User ID

1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Start the bot
3. Copy your ID

## Local Testing

For local testing, set in `.env`:

```env
V2RAY_CONFIG_PATH=./config.json
DATABASE_PATH=./data/v2ray_accounts.db
```

## Production Deployment

1. Upload project to VPS
2. Install V2Ray
3. Configure SSL certificates
4. Update `.env` with production paths
5. Run with systemd service

## License

MIT
