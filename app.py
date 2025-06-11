import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/extract", methods=["POST"])
def extract():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "Geen tekst ontvangen"}), 400

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": (
                "Je bent een assistent die informatie uit Nederlandse chattekst haalt. "
                "Geef per gevonden element een regel die begint met 'kl' en alleen de inhoud (zonder categorie). "
                "Eindig op elke regel met precies één item. "
                "Voorbeeld:\nInput: 'Ik heet Laura, ik werk als verpleegkundige en wandel graag.'\nOutput:\nklLaura\nklverpleegkundige\nklwandelen"
            )},
            {"role": "user", "content": text}
        ],
        temperature=0.5,
        max_tokens=100
    )
    response = completion.choices[0].message.content.strip()
    return jsonify({"lines": response.splitlines()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
