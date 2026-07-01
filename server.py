from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

def load_keys():
    if not os.path.exists("keys.json"):
        return {}

    with open("keys.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()

    key = data.get("key")
    device = data.get("device")

    keys = load_keys()

    if key not in keys:
        return jsonify({"status": False, "message": "Key không tồn tại"})

    if keys[key]["device"] != device:
        return jsonify({"status": False, "message": "Sai Device ID"})

    return jsonify({
        "status": True,
        "message": "Key hợp lệ"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
@app.route("/add", methods=["POST"])
def add_key():
    data = request.get_json()

    key = data.get("key")
    device = data.get("device", "")
    date = data.get("date")

    keys = load_keys()

    keys[key] = {
        "device": device,
        "date": date
    }

    with open("keys.json", "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=4)

    return jsonify({
        "status": True,
        "message": "Đã thêm key"
    })    