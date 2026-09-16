import os
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL = os.environ.get("TELEGRAM_CHANNEL")

@app.get("/")
def home():
    return "Schoolvision bridge is running"

@app.post("/publish")
def publish():
    data = request.json or {}
    return {"ok": True, "message": "Bridge received the post"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
