"""
Database manager for account operations
"""
import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from .models import Account

UUID_NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')


class Database:
    """Database operations manager"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                limit_type TEXT NOT NULL,
                data_limit INTEGER,
                expire_date TEXT,
                created_date TEXT NOT NULL,
                total_traffic INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active'
            )
        """)
        conn.commit()
        conn.close()
    
    def create_account(self, email: str, limit_type: str, 
                      data_limit: Optional[int] = None, 
                      days: Optional[int] = None) -> Optional[Account]:
        """Create new account"""
        account_uuid = str(uuid.uuid5(UUID_NAMESPACE, email))
        created = datetime.now().isoformat()
        expire_date = None
        
        if limit_type == "time" and days:
            expire_date = (datetime.now() + timedelta(days=days)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO accounts (uuid, email, limit_type, data_limit, expire_date, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (account_uuid, email, limit_type, data_limit, expire_date, created))
            conn.commit()
            
            return Account(
                id=cursor.lastrowid,
                uuid=account_uuid,
                email=email,
                limit_type=limit_type,
                data_limit=data_limit,
                expire_date=expire_date,
                created_date=created
            )
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_account(self, email: str) -> Optional[Account]:
        """Get account by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Account(*row)
        return None
    
    def list_accounts(self) -> List[Account]:
        """List all accounts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts ORDER BY created_date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [Account(*row) for row in rows]
    
    def delete_account(self, email: str) -> bool:
        """Delete account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE email = ?", (email,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    
    def update_traffic(self, email: str, traffic: int):
        """Update traffic usage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET total_traffic = total_traffic + ? WHERE email = ?",
            (traffic, email)
        )
        conn.commit()
        conn.close()
    
    def update_status(self, email: str, status: str):
        """Update account status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET status = ? WHERE email = ?",
            (status, email)
        )
        conn.commit()
        conn.close()