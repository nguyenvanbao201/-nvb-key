import sqlite3

conn = sqlite3.connect("keys.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS keys(
id INTEGER PRIMARY KEY AUTOINCREMENT,
key TEXT UNIQUE,
created_at TEXT,
expires_at TEXT
)
""")

conn.commit()
conn.close()

print("Database OK")