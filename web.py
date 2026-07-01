from flask import Flask
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>VB Tool Key</h1>
    <p>Web hoạt động thành công.</p>
    """

@app.route("/key/<token>")
def show_key(token):
    conn = sqlite3.connect("key.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT key_value, expires_at FROM keys WHERE token=?",
        (token,)
    )

    row = cur.fetchone()
    conn.close()

    if row is None:
        return "<h2>❌ Key không tồn tại.</h2>"

    key, expires = row

    if datetime.now() > datetime.strptime(expires, "%Y-%m-%d %H:%M:%S"):
        return "<h2>⏰ Key đã hết hạn.</h2>"

    return f"""
    <h1>🎉 Key của bạn</h1>
    <h2>{key}</h2>
    <p>Có hiệu lực đến: {expires}</p>
    """

app.run(host="0.0.0.0", port=5000)
