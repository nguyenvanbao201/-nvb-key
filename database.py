import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("keys.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS keys(
    telegram_id TEXT,
    key TEXT,
    expire_at TEXT
)
""")

conn.commit()


def save_key(user_id, key):
    expire = datetime.now() + timedelta(hours=24)

    cur.execute(
        "INSERT INTO keys VALUES (?,?,?)",
        (
            str(user_id),
            key,
            expire.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()


def check_key(key):
    cur.execute(
        "SELECT expire_at FROM keys WHERE key=?",
        (key,),
    )

    row = cur.fetchone()

    if not row:
        return False

    expire = datetime.strptime(
        row[0],
        "%Y-%m-%d %H:%M:%S"
    )

    return datetime.now() < expire


def check_user(user_id):
    cur.execute(
        "SELECT expire_at FROM keys WHERE telegram_id=? ORDER BY expire_at DESC LIMIT 1",
        (str(user_id),),
    )

    row = cur.fetchone()

    if not row:
        return False

    expire = datetime.strptime(
        row[0],
        "%Y-%m-%d %H:%M:%S"
    )

    return datetime.now() < expire