"""
Database models and schema definitions
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Account:
    """Account model"""
    id: Optional[int] = None
    uuid: str = ""
    email: str = ""
    limit_type: str = ""  # 'data' or 'time'
    data_limit: Optional[int] = None  # in GB
    expire_date: Optional[str] = None
    created_date: str = ""
    total_traffic: int = 0  # in bytes
    status: str = "active"  # 'active' or 'disabled'
    
    def is_expired(self) -> bool:
        """Check if account is expired"""
        if self.limit_type == "time" and self.expire_date:
            expire = datetime.fromisoformat(self.expire_date)
            return datetime.now() > expire
        return False
    
    def is_over_limit(self) -> bool:
        """Check if account exceeded data limit"""
        if self.limit_type == "data" and self.data_limit:
            return self.total_traffic >= (self.data_limit * 1024 * 1024 * 1024)
        return False
    
    def get_remaining_data(self) -> Optional[float]:
        """Get remaining data in GB"""
        if self.limit_type == "data" and self.data_limit:
            used_gb = self.total_traffic / (1024 * 1024 * 1024)
            return max(0, self.data_limit - used_gb)
        return None
    
    def get_remaining_days(self) -> Optional[int]:
        """Get remaining days"""
        if self.limit_type == "time" and self.expire_date:
            expire = datetime.fromisoformat(self.expire_date)
            delta = expire - datetime.now()
            return max(0, delta.days)
        return None