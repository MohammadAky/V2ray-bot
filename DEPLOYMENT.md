# VPS Deployment Guide for V2ray Bot

## Prerequisites
- Ubuntu 20.04+ or Debian 11+ VPS
- Root or sudo access
- At least 512MB RAM, 10GB storage
- Static IP address

## Step 1: Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git python3 python3-pip ufw unzip gnupg2
```

## Step 2: Install Xray
```bash
# Install Xray core
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# Enable and start Xray service
sudo systemctl enable xray
sudo systemctl start xray
```

## Step 3: Clone and Setup Project
```bash
# Clone repository
git clone https://github.com/MohammadAky/V2ray-bot.git
cd V2ray-bot

# Install Python dependencies
pip3 install -r requirements.txt
```

## Step 4: Configure Environment
```bash
# Create .env file
nano .env

# Add the following (replace with your values):
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
SERVER_ADDRESS=your_vps_ip_address
SERVER_PORT=443
REALITY_PRIVATE_KEY=your_generated_private_key
REALITY_PUBLIC_KEY=your_generated_public_key
REALITY_SHORT_ID=your_short_id
```

## Step 5: Generate Reality Keys
```bash
# Download Xray binary for key generation
wget https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip
unzip Xray-linux-64.zip
chmod +x xray

# Generate X25519 keys (run this command)
./xray x25519

# Example output:
# Private key: abc123...
# Public key: def456...
```

## Step 6: Configure Firewall
```bash
# Allow necessary ports
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Check status
sudo ufw status
```

## Step 7: Setup SSL Certificate (Optional but Recommended)
```bash
# Install certbot for Let's Encrypt
sudo apt install -y certbot

# Get certificate (replace domain.com with your domain)
# sudo certbot certonly --standalone -d your-domain.com

# Note: For IP-based Reality, SSL certificates are not strictly necessary
```

## Step 8: Install Node.js and Run the Bot
```bash
# Install Node.js (required for PM2)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify Node.js installation
node --version
npm --version

# Install PM2 for process management
sudo npm install -g pm2

# Start the bot
pm2 start main.py --name v2ray-bot

# Setup PM2 to start on boot
pm2 startup
pm2 save

# Check status
pm2 status
```

## Step 9: Verify Installation
```bash
# Check Xray status
sudo systemctl status xray

# Check bot logs
pm2 logs v2ray-bot

# Test Xray configuration
sudo xray -test -config config.json
```

## Step 10: Monitor and Maintain
```bash
# View real-time logs
pm2 logs v2ray-bot --lines 50

# Restart services
sudo systemctl restart xray
pm2 restart v2ray-bot

# Update bot
cd V2ray-bot
git pull origin main
pm2 restart v2ray-bot
```

## Troubleshooting

### Xray Issues
```bash
# Test configuration
sudo xray -test -config config.json

# Check if port 443 is in use
sudo netstat -tlnp | grep :443

# View Xray logs
sudo journalctl -u xray -f
```

### Bot Issues
```bash
# Check bot logs
pm2 logs v2ray-bot

# Restart bot
pm2 restart v2ray-bot

# Check environment variables
cat .env
```

### Network Issues
```bash
# Check firewall
sudo ufw status

# Test port connectivity
telnet your_server_ip 443

# Check if Xray is listening
sudo netstat -tlnp | grep xray
```

## Security Recommendations

1. **Change SSH port** from default 22
2. **Use SSH keys** instead of passwords
3. **Enable fail2ban** for SSH protection
4. **Keep system updated**: `sudo apt update && sudo apt upgrade`
5. **Monitor logs regularly**

## Backup Strategy

```bash
# Backup important files
tar -czf backup_$(date +%Y%m%d).tar.gz \
  config.json \
  data/ \
  .env

# Backup database regularly
cp data/v2ray_accounts.db data/v2ray_accounts_backup.db
```

## Performance Tuning

1. **Enable BBR** for better TCP performance:
   ```bash
   echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
   echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
   sysctl -p
   ```

2. **Optimize kernel parameters** for high concurrency

Your V2ray Reality bot is now ready for production! 🚀
