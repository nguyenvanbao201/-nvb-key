from flask import Flask, request, jsonify
import json
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

# Hàm tạo key ngẫu nhiên
def create_key():
    chars = string.ascii_uppercase + string.digits
    return "TBTOOL-" + "".join(random.choice(chars) for _ in range(8))

@app.route("/")
def home():
    return "VBTOOL KEY SERVER"

@app.route("/create_free_key", methods=["GET", "POST"])
def create_free_key():
    data = request.json
    device_id = data["device_id"]

    # Đọc file keys.json
    try:
        with open("keys.json", "r") as f:
            keys = json.load(f)
    except:
        keys = {}

    # Tạo key mới
    key = create_key()

    # Lưu key
    keys[key] = {
        "device_id": device_id,
        "used": False,
        "type": "FREE",
        "expire": (datetime.now() + timedelta(days=1)).isoformat()
    }

    with open("keys.json", "w") as f:
        json.dump(keys, f, indent=4)

    return jsonify({
        "success": True,
        "key": key
    })

if __name__ == "__main__":
    app.run()
