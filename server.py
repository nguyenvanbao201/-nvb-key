from flask import Flask, request, jsonify
import sqlite3
import random
import string
import time

app = Flask(__name__)

DB = "keys.db"

def get_db():
    return sqlite3.connect(DB)

def create_code():
    return "VB-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=16))

@app.route("/issue-code", methods=["POST"])
def issue_code():
    code = create_code()
    expire = int(time.time()) + 86400  # 24 giờ

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO keys(code, expire) VALUES(?, ?)",
        (code, expire)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "code": code,
        "expire": expire
    })

@app.route("/verify-code", methods=["POST"])
def verify_code():
    data = request.get_json(silent=True) or {}
    code = data.get("code")

    if not code:
        return jsonify({"success": False, "message": "Thiếu code"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT expire FROM keys WHERE code=?",
        (code,)
    )

    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({
            "success": False,
            "message": "Code không tồn tại"
        })

    if int(time.time()) > row[0]:
        return jsonify({
            "success": False,
            "message": "Code đã hết hạn"
        })

    return jsonify({
        "success": True,
        "message": "Code hợp lệ"
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )