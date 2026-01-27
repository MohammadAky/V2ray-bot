"""
Generate client configuration links for Xray Reality
"""
import json
import base64
from urllib.parse import quote
from config.settings import SERVER_ADDRESS, SERVER_PORT, REALITY_SERVER_NAMES


class ClientConfigGenerator:
    """Generate client configuration links for Xray Reality"""

    @staticmethod
    def generate_vless_link(email: str, client_uuid: str, reality_keys: dict = None) -> str:
        """Generate vless:// link for Reality client"""
        # VLESS URL format: vless://uuid@server:port?type=tcp&security=reality&pbk=public_key&sni=server_name&sid=short_id&spx=%2F&flow=xtls-rprx-vision#remark

        if reality_keys:
            public_key = reality_keys.get('public_key', '')
            short_id = reality_keys.get('short_id', '')
            sni = REALITY_SERVER_NAMES[0] if REALITY_SERVER_NAMES else 'www.google.com'
        else:
            public_key = ''
            short_id = ''
            sni = 'www.google.com'

        params = {
            'type': 'tcp',
            'security': 'reality',
            'pbk': public_key,
            'sni': sni,
            'sid': short_id,
            'spx': '/',
            'flow': 'xtls-rprx-vision'
        }

        query_string = '&'.join([f"{k}={quote(str(v))}" for k, v in params.items() if v])
        return f"vless://{client_uuid}@{SERVER_ADDRESS}:{SERVER_PORT}?{query_string}#{quote(email)}"

    @staticmethod
    def generate_qr_text(vless_link: str) -> str:
        """Generate text for QR code"""
        return vless_link