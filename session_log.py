import sqlite3
from datetime import datetime, timedelta
import pytz

class SessionLogger:
    def __init__(self, db_path="session_log.db"):
        self.conn = sqlite3.connect(db_path)
        self.tz = pytz.timezone("America/Toronto")
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    role TEXT,
                    text TEXT
                )
            """)

    def _now(self):
        """Return current time in Toronto timezone as ISO string."""
        return datetime.now(self.tz).isoformat()

    def log(self, role, text):
        timestamp = self._now()
        with self.conn:
            self.conn.execute(
                "INSERT INTO log (timestamp, role, text) VALUES (?, ?, ?)",
                (timestamp, role, text)
            )

    def get_last_n(self, n=5):
        cursor = self.conn.execute(
            "SELECT role, text FROM log ORDER BY id DESC LIMIT ?", (n,)
        )
        return list(reversed(cursor.fetchall()))

    def get_by_day(self, days_ago=0):
        today = datetime.now(self.tz).date()
        target_date = today - timedelta(days=days_ago)
        start = datetime.combine(target_date, datetime.min.time())
        end = datetime.combine(target_date, datetime.max.time())
        start_iso = self.tz.localize(start).isoformat()
        end_iso = self.tz.localize(end).isoformat()

        cursor = self.conn.execute(
            "SELECT timestamp, role, text FROM log WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp ASC",
            (start_iso, end_iso)
        )
        return cursor.fetchall()
    
    def get_full_log(self, n=10, show_time=True):
        cursor = self.conn.execute(
            "SELECT timestamp, role, text FROM log ORDER BY id DESC LIMIT ?", (n,)
        )
        results = list(reversed(cursor.fetchall()))  # oldest → newest

        if not show_time:
            return [(role, text) for _, role, text in results]

        # Format the time for readability
        formatted = []
        for timestamp, role, text in results:
            dt = datetime.fromisoformat(timestamp)
            readable_time = dt.strftime("%b %d, %I:%M %p")  # e.g., May 19, 02:13 PM
            formatted.append((readable_time, role, text))

        return formatted

    def count_entries(self):
        cursor = self.conn.execute("SELECT COUNT(*) FROM log")
        count = cursor.fetchone()[0]
        return count

    def get_logs_between(self, start_time, end_time):
        cursor = self.conn.execute(
            "SELECT timestamp, role, text FROM log WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp ASC",
            (start_time.isoformat(), end_time.isoformat())
        )
        return cursor.fetchall()


if __name__=="__main__":
    logger = SessionLogger()
    
    for entry in logger.get_full_log(5):
        print(entry)
    
    print("Total log entries:", logger.count_entries())
