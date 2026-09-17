import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL = os.environ.get("TELEGRAM_CHANNEL")
SECRET = os.environ.get("BRIDGE_SECRET")


@app.get("/")
def home():
    return "Schoolvision bridge is running"


@app.post("/publish")
def publish():
    if request.headers.get("X-Bridge-Secret") != SECRET:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    data = request.json or {}
    text = data.get("text")

    if not text:
        return jsonify({"ok": False, "error": "No text"}), 400

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHANNEL,
            "text": text
        },
        timeout=20
    )

    return jsonify(response.json())

@app.get("/test")
def test():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={
            "chat_id": CHANNEL,
            "text": "🟢 Тест Schoolvision — бот работает!"
        },
        timeout=20
    )
    return response.json()
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
