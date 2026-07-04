import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("keys.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS keys(
    key TEXT PRIMARY KEY,
    telegram_id TEXT,
    created_at TEXT,
    expire_at TEXT
)
""")

conn.commit()


def save_key(key, telegram_id):
    created = datetime.now()
    expire = created + timedelta(hours=24)

    cur.execute(
        "INSERT INTO keys VALUES (?,?,?,?)",
        (
            key,
            str(telegram_id),
            created.strftime("%Y-%m-%d %H:%M:%S"),
            expire.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()


def check_key(key):
    cur.execute("SELECT expire_at FROM keys WHERE key=?", (key,))
    row = cur.fetchone()

    if not row:
        return False

    expire = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")

    return datetime.now() < expire