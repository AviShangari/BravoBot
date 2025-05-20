import sqlite3
import os

class MemoryStore:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

    def remember(self, key, value):
        with self.conn:
            self.conn.execute("REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))

    def recall(self, key):
        cursor = self.conn.execute("SELECT value FROM memory WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else None

    def forget(self, key):
        with self.conn:
            self.conn.execute("DELETE FROM memory WHERE key = ?", (key,))

    def list_all(self):
        cursor = self.conn.execute("SELECT key, value FROM memory")
        return cursor.fetchall()

# Example test
if __name__ == "__main__":
    mem = MemoryStore()
    mem.remember("favorite_music", "Lo-Fi")
    print("Favorite Music:", mem.recall("favorite_music"))
    mem.remember("user_name", "Aaveg")
    print("All memory:", mem.list_all())
    mem.forget("favorite_music")
    print("After forgetting:", mem.list_all())
