from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "VB TOOL API"

@app.route("/api/get_key")
def get_key():
    return jsonify({
        "status": "success",
        "key": "LOTTO-TEST-1234-5678-9999"
    })

if __name__ == "__main__":
    app.run()