import sqlite3

conn = sqlite3.connect("key.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    token TEXT,
    key_value TEXT,
    expires_at TEXT
)
""")

conn.commit()