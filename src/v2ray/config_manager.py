"""
Xray configuration file manager with Reality protocol
"""
import json
import uuid
from pathlib import Path
from typing import Dict, Any

from config.settings import (
    XRAY_CONFIG_PATH, SERVER_PORT, CERT_FILE, KEY_FILE,
    REALITY_PRIVATE_KEY, REALITY_PUBLIC_KEY, REALITY_SHORT_ID,
    REALITY_SERVER_NAMES, SERVER_ADDRESS
)


class XrayConfigManager:
    """Manage Xray configuration file with Reality protocol"""

    def __init__(self, config_path: str = XRAY_CONFIG_PATH):
        self.config_path = Path(config_path)
        self.ensure_config_exists()
    
    def ensure_config_exists(self):
        """Create base config if not exists"""
        if not self.config_path.exists():
            base_config = self._get_base_config()
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_config(base_config)
    
    def _get_base_config(self) -> Dict[str, Any]:
        """Get base Xray configuration with Reality protocol"""
        # Generate keys if not provided
        private_key = REALITY_PRIVATE_KEY or self._generate_private_key()
        public_key = REALITY_PUBLIC_KEY or self._generate_public_key()
        short_id = REALITY_SHORT_ID or self._generate_short_id()

        return {
            "log": {
                "loglevel": "warning"
            },
            "inbounds": [{
                "port": SERVER_PORT,
                "protocol": "vless",
                "settings": {
                    "clients": [],
                    "decryption": "none"
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "reality",
                    "realitySettings": {
                        "show": False,
                        "dest": "www.google.com:443",  # Use Google as it's more universally accessible
                        "serverNames": ["www.google.com", "www.microsoft.com"],
                        "privateKey": private_key,
                        "shortIds": [short_id],
                        "publicKey": public_key
                    }
                }
            }],
            "outbounds": [{
                "protocol": "freedom",
                "settings": {}
            }],
            "policy": {
                "levels": {
                    "0": {
                        "handshake": 4,
                        "connIdle": 300,
                        "uplinkOnly": 2,
                        "downlinkOnly": 5,
                        "statsUserUplink": True,
                        "statsUserDownlink": True,
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
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def add_client(self, email: str, client_uuid: str):
        """Add client to Xray Reality config"""
        config = self._load_config()

        client = {
            "id": client_uuid,
            "email": email,
            "flow": "xtls-rprx-vision"
        }

        config['inbounds'][0]['settings']['clients'].append(client)
        self._save_config(config)
    
    def remove_client(self, email: str):
        """Remove client from V2Ray config"""
        config = self._load_config()
        
        clients = config['inbounds'][0]['settings']['clients']
        config['inbounds'][0]['settings']['clients'] = [
            c for c in clients if c['email'] != email
        ]
        
        self._save_config(config)

    def client_exists(self, email: str) -> bool:
        """Check if client exists in config"""
        config = self._load_config()
        clients = config['inbounds'][0]['settings']['clients']
        return any(c.get('email', '') == email for c in clients)

    def _generate_private_key(self) -> str:
        """Generate a random private key for Reality"""
        return str(uuid.uuid4()).replace('-', '')[:32]

    def _generate_public_key(self) -> str:
        """Generate a random public key for Reality"""
        return str(uuid.uuid4()).replace('-', '')[:32]

    def _generate_short_id(self) -> str:
        """Generate a random short ID for Reality"""
        return str(uuid.uuid4()).replace('-', '')[:8]

    def get_reality_keys(self) -> Dict[str, str]:
        """Get Reality keys from current config"""
        config = self._load_config()
        reality_settings = config['inbounds'][0]['streamSettings']['realitySettings']
        return {
            'private_key': reality_settings['privateKey'],
            'public_key': reality_settings.get('publicKey', 'generated_public_key'),  # In real implementation, this should be derived
            'short_id': reality_settings['shortIds'][0]
        }