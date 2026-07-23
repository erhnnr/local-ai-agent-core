import sqlite3
import os

class DatabaseManager:
    """
    Motorun karar geçmişini, parametrelerini ve verilerini saklayan SQLite yöneticisi.
    """
    def __init__(self, db_name: str = "data/decision_engine.db"):
        # data klasörünün olduğundan emin olalım
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.db_name = db_name
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        """Gerekli tabloları oluşturur."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decision_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
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