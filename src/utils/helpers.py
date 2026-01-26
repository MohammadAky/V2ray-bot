"""
Helper utilities
"""
from datetime import datetime


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_date(date_str: str) -> str:
    """Format ISO date to readable format"""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return date_str


def get_status_emoji(status: str) -> str:
    """Get emoji for status"""
    return "✅" if status == "active" else "❌"