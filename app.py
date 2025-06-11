from flask import Flask, request, jsonify
from openai import OpenAI
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# OpenAI client initialiseren met API key uit environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages")
    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # App draaien op poort 5000 en alle interfaces openzetten
    app.run(host="0.0.0.0", port=5000)
