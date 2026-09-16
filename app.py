import os
import hmac
import json
import urllib.parse
import urllib.request

from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHANNEL = os.environ.get("TELEGRAM_CHANNEL", "")
BRIDGE_SECRET = os.environ.get("BRIDGE_SECRET", "")


@app.get("/")
def home():
    return "Schoolvision bridge is running"


@app.post("/publish")
def publish():
    # Защита от посторонних запросов
    provided_secret = request.headers.get("X-Bridge-Secret", "")

    if not BRIDGE_SECRET or not hmac.compare_digest(provided_secret, BRIDGE_SECRET):
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()

    if not text:
        return jsonify({"ok": False, "error": "Text is empty"}), 400

    if not TELEGRAM_TOKEN or not TELEGRAM_CHANNEL:
        return jsonify({
            "ok": False,
            "error": "Telegram settings are missing"
        }), 500

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHANNEL,
        "text": text
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, method="POST")

        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
