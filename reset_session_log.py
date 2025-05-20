import sqlite3

conn = sqlite3.connect("session_log.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM log;")  # Deletes all rows
conn.commit()
conn.close()

print("session_log.db has been wiped clean.")
