import os
import sqlite3


class DatabaseManager:
    """
    Motorun karar geçmişini, sohbet mesajlarını ve verilerini saklayan SQLite yöneticisi.
    """
    def __init__(self, db_name: str = "data/decision_engine.db"):
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.db_name = db_name
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        """Gerekli tabloları oluşturur."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Karar günlükleri tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decision_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Sohbet geçmişi tablosu (Hafıza için)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_decision(self, prompt: str, response: str):
        """Yapılan bir karar/sorgu işlemini veritabanına kaydeder."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO decision_logs (prompt, response) VALUES (?, ?)",
                (prompt, response)
            )
            conn.commit()

    def get_recent_decisions(self, limit: int = 5):
        """Son yapılan kararları getirir."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT prompt, response, timestamp FROM decision_logs ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()

    def save_chat_message(self, role: str, content: str):
        """Sohbet mesajını veritabanına kaydeder (user veya assistant)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (role, content) VALUES (?, ?)",
                (role, content)
            )
            conn.commit()

    def get_chat_history(self, limit: int = 20):
        """Geçmiş sohbet mesajlarını kronolojik sırayla getirir."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM (SELECT role, content, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT ?) ORDER BY timestamp ASC",
                (limit,)
            )
            return cursor.fetchall()