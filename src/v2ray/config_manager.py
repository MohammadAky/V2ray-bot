"""
V2Ray configuration file manager
"""
import json
from pathlib import Path
from typing import Dict, Any

from config.settings import V2RAY_CONFIG_PATH, SERVER_PORT, CERT_FILE, KEY_FILE


class V2RayConfigManager:
    """Manage V2Ray configuration file"""
    
    def __init__(self, config_path: str = V2RAY_CONFIG_PATH):
        self.config_path = Path(config_path)
        self.ensure_config_exists()
    
    def ensure_config_exists(self):
        """Create base config if not exists"""
        if not self.config_path.exists():
            base_config = self._get_base_config()
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_config(base_config)
    
    def _get_base_config(self) -> Dict[str, Any]:
        """Get base V2Ray configuration"""
        return {
            "log": {
                "loglevel": "warning"
            },
            "inbounds": [{
                "port": SERVER_PORT,
                "protocol": "vmess",
                "settings": {
                    "clients": []
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "tls",
                    "tlsSettings": {
                        "certificates": [{
                            "certificateFile": CERT_FILE,
                            "keyFile": KEY_FILE
                        }]
                    }
                }
            }],
            "outbounds": [{
                "protocol": "freedom",
                "settings": {}
            }]
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
        """Add client to V2Ray config"""
        config = self._load_config()
        
        client = {
            "id": client_uuid,
            "email": email,
            "alterId": 0
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
        return any(c['email'] == email for c in clients)