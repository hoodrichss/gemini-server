from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="

@app.route("/", methods=["GET"])
def home():
    return {"status": "Gemini proxy server is running."}

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    if API_KEY is None:
        return jsonify({"error": "API key not configured"}), 500

    user_payload = request.json

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_payload["messages"][-1]["content"]}
                ]
            }
        ]
    }

    r = requests.post(
        GEMINI_URL + API_KEY,
        json=payload
    )

    data = r.json()

    try:
        output_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        output_text = str(data)

    return jsonify({
        "id": "chatcmpl-gemini",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": output_text
            },
            "finish_reason": "stop"
        }]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
