from flask import Flask, request
from database import save_key, check_key
import random
import string

app = Flask(__name__)

def tao_key():
    return "LOTTO-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=16)
    )

@app.route("/")
def home():
    return "<h2>VB Tool Key Server</h2>"

@app.route("/generate")
def generate():
    telegram_id = request.args.get("id", "guest")

    key = tao_key()

    save_key(telegram_id, key)

    return f"""
    <html>
    <head>
        <title>KEY</title>
    </head>
    <body style="font-family:Arial;text-align:center;margin-top:80px">
        <h1>🔑 KEY CỦA BẠN</h1>
        <h2>{key}</h2>
        <p>⏰ Có hiệu lực 24 giờ</p>
    </body>
    </html>
    """

@app.route("/check")
def check():
    key = request.args.get("key", "")

    if check_key(key):
        return {"valid": True}
    else:
        return {"valid": False}

if __name__ == "__main__":
    app.run(debug=True)