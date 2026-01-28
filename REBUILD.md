# 🚀 Complete V2ray Reality Bot Rebuild Guide

## Prerequisites
- Ubuntu 20.04+ or Debian 11+ VPS
- Root or sudo access
- At least 512MB RAM, 10GB storage
- Static IP address

---

## Step 1: Clean Server Setup

### 1.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

### 1.2 Install Dependencies
```bash
sudo apt install -y curl wget git python3 python3-pip ufw unzip gnupg2
```

### 1.3 Configure Firewall
```bash
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
sudo ufw status
```

---

## Step 2: Install Xray Core

### 2.1 Download and Install Xray
```bash
# Remove any existing Xray
sudo systemctl stop xray 2>/dev/null || true
sudo systemctl disable xray 2>/dev/null || true
sudo rm -rf /usr/local/bin/xray /usr/local/share/xray /etc/systemd/system/xray.service

# Install fresh Xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# Verify installation
xray version
```

### 2.2 Enable and Start Xray
```bash
sudo systemctl enable xray
sudo systemctl start xray
sudo systemctl status xray
```

---

## Step 3: Generate Reality Keys

### 3.1 Generate Fresh X25519 Keys
```bash
# Generate new keys (save these!)
./xray x25519

# Example output:
# Private key: UMCEnxBHve8FSRSRpgsjXLOMm3bfc7p2GMnWgtc7TVg
# Public key: ABeILk5qbD7h8Jo9_UnTacqEJrgqCpwqmQL7zpFQ3gw
# Short ID: (you can use any 8-character string)
```

### 3.2 Save Your Keys
**Important**: Save these keys securely. You'll need them for the config.

---

## Step 4: Deploy V2ray Bot

### 4.1 Clone Repository
```bash
# Remove old installation if exists
sudo rm -rf /opt/V2ray-bot

# Clone fresh
git clone https://github.com/MohammadAky/V2ray-bot.git /opt/V2ray-bot
cd /opt/V2ray-bot
```

### 4.2 Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

---

## Step 5: Configure Environment

### 5.1 Create .env File
```bash
nano .env
```

**Add this content (replace with your actual values):**
```env
# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321

# Server Configuration
SERVER_ADDRESS=your_vps_ip_address
SERVER_PORT=443

# Xray Configuration Path
XRAY_CONFIG_PATH=config.json
DATABASE_PATH=data/v2ray_accounts.db

# Reality Protocol Settings (IP-based, no domain required)
REALITY_PRIVATE_KEY=UMCEnxBHve8FSRSRpgsjXLOMm3bfc7p2GMnWgtc7TVg
REALITY_PUBLIC_KEY=ABeILk5qbD7h8Jo9_UnTacqEJrgqCpwqmQL7zpFQ3gw
REALITY_SHORT_ID=abcd1234

# Optional: Custom Reality Server Names
REALITY_SERVER_NAMES=www.google.com,www.microsoft.com
```

---

## Step 6: Create Xray Configuration

### 6.1 Create config.json
```bash
nano config.json
```

**Paste this complete configuration:**
```json
{
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "show": false,
          "dest": "www.google.com:443",
          "serverNames": [
            "www.google.com",
            "www.microsoft.com"
          ],
          "privateKey": "UMCEnxBHve8FSRSRpgsjXLOMm3bfc7p2GMnWgtc7TVg",
          "publicKey": "ABeILk5qbD7h8Jo9_UnTacqEJrgqCpwqmQL7zpFQ3gw",
          "shortIds": [
            "abcd1234"
          ]
        }
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "settings": {}
    }
  ],
  "policy": {
    "levels": {
      "0": {
        "handshake": 4,
        "connIdle": 300,
        "uplinkOnly": 2,
        "downlinkOnly": 5,
        "statsUserUplink": true,
        "statsUserDownlink": true,
        "bufferSize": 4096
      }
    }
  },
  "routing": {
    "rules": [
      {
        "type": "field",
        "outboundTag": "direct",
        "domain": ["geosite:category-ads-all"]
      }
    ]
  }
}
```

### 6.2 Test Xray Configuration
```bash
sudo xray -test -config config.json
```

**Expected output:**
```
Xray 26.1.23 (Xray, Penetrates Everything.) ...
Configuration OK.
```

---

## Step 7: Setup Database

### 7.1 Create Database Directory
```bash
mkdir -p data
chmod 755 data
```

### 7.2 Initialize Database
The database will be created automatically when the bot first runs.

---

## Step 8: Install Node.js and PM2

### 8.1 Install Node.js
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 8.2 Install PM2
```bash
sudo npm install -g pm2
pm2 --version
```

---

## Step 9: Start the Bot

### 9.1 Start with PM2
```bash
cd /opt/V2ray-bot
pm2 start main.py --name v2ray-bot
```

### 9.2 Setup Auto-start
```bash
pm2 startup
pm2 save
```

### 9.3 Check Status
```bash
pm2 status
pm2 logs v2ray-bot --lines 20
```

---

## Step 10: Test Everything

### 10.1 Verify Services
```bash
# Check Xray
sudo systemctl status xray

# Check bot
pm2 status

# Check ports
sudo netstat -tlnp | grep :443
```

### 10.2 Test Bot Functionality
1. Send `/start` to your bot on Telegram
2. Try creating an account: `/add ali@example.com daily`
3. Check if you receive a working VLESS link

### 10.3 Test VLESS Connection
Import the generated VLESS link into a V2ray/Xray client and test the connection.

---

## Troubleshooting

### Issue: Xray config test fails
```bash
# Check JSON syntax
python3 -c "import json; json.load(open('config.json')); print('JSON OK')"

# Check file permissions
ls -la config.json
```

### Issue: Bot won't start
```bash
# Check Python dependencies
pip3 list | grep -E "(python-telegram-bot|sqlalchemy)"

# Check .env file
cat .env

# Check logs
pm2 logs v2ray-bot --lines 50
```

### Issue: VLESS links don't work
```bash
# Verify Reality keys in config.json match .env
grep -A 5 "realitySettings" config.json

# Test Xray is running on port 443
sudo netstat -tlnp | grep :443
```

### Issue: Database errors
```bash
# Check database permissions
ls -la data/
chmod 755 data/
```

---

## Security Hardening

### Change SSH Port (Optional but Recommended)
```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config
# Change: Port 22 → Port 2222

# Update firewall
sudo ufw allow 2222
sudo ufw delete allow ssh

# Restart SSH
sudo systemctl restart ssh

# Test new port before closing terminal
ssh -p 2222 user@your-server
```

### Setup Fail2Ban
```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## Backup & Recovery

### Create Backup Script
```bash
nano /opt/V2ray-bot/backup.sh
```

**Add this content:**
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup configurations
tar -czf $BACKUP_DIR/v2ray_config_$DATE.tar.gz \
  /opt/V2ray-bot/config.json \
  /opt/V2ray-bot/.env \
  /opt/V2ray-bot/data/

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz \
  /opt/V2ray-bot/logs/ \
  ~/.pm2/logs/

echo "Backup completed: $BACKUP_DIR/v2ray_config_$DATE.tar.gz"
```

```bash
chmod +x /opt/V2ray-bot/backup.sh
```

### Schedule Daily Backups
```bash
# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /opt/V2ray-bot/backup.sh
```

---

## Monitoring & Maintenance

### Check System Resources
```bash
# Memory usage
free -h

# Disk usage
df -h

# Network connections
sudo netstat -tlnp | grep xray
```

### Update the Bot
```bash
cd /opt/V2ray-bot
git pull origin main
pm2 restart v2ray-bot
```

### Log Rotation
```bash
# PM2 logs
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

---

## ✅ Success Checklist

- [ ] Server updated and secured
- [ ] Xray installed and running
- [ ] Reality keys generated and configured
- [ ] Bot cloned and dependencies installed
- [ ] Environment configured (.env)
- [ ] Xray config tested and working
- [ ] Database initialized
- [ ] PM2 installed and bot running
- [ ] Telegram bot responds to commands
- [ ] VLESS links generated correctly
- [ ] Client connections work
- [ ] Backups configured
- [ ] Monitoring in place

---

## 🎯 Quick Commands Reference

```bash
# Status checks
sudo systemctl status xray
pm2 status

# Logs
pm2 logs v2ray-bot
sudo journalctl -u xray -f

# Restarts
sudo systemctl restart xray
pm2 restart v2ray-bot

# Updates
cd /opt/V2ray-bot && git pull origin main
```

**Your V2ray Reality bot is now fully configured and ready for production! 🚀**

---

*Last updated: January 2026*
*Tested with Xray 26.1.23 and Ubuntu 20.04*
