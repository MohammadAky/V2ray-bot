"""
Generate client configuration links
"""
import json
import base64
from config.settings import SERVER_ADDRESS, SERVER_PORT


class ClientConfigGenerator:
    """Generate client configuration links"""
    
    @staticmethod
    def generate_vmess_link(email: str, client_uuid: str) -> str:
        """Generate vmess:// link for client"""
        vmess_config = {
            "v": "2",
            "ps": email,
            "add": SERVER_ADDRESS,
            "port": str(SERVER_PORT),
            "id": client_uuid,
            "aid": "0",
            "net": "tcp",
            "type": "none",
            "host": "",
            "path": "",
            "tls": ""  # Changed from "tls" to empty string
        }
    
        config_str = json.dumps(vmess_config)
        encoded = base64.b64encode(config_str.encode()).decode()
        return f"vmess://{encoded}"

    @staticmethod
    def generate_qr_text(vmess_link: str) -> str:
        """Generate text for QR code (if needed later)"""
        return vmess_link