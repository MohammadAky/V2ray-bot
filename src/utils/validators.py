"""
Input validation utilities
"""
import re


class Validator:
    """Input validation"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_limit_type(limit_type: str) -> bool:
        """Validate limit type"""
        return limit_type.lower() in ['data', 'time']
    
    @staticmethod
    def is_positive_integer(value: str) -> bool:
        """Check if value is positive integer"""
        try:
            return int(value) > 0
        except ValueError:
            return False