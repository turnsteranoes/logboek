from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Je krijgt een kort stukje tekst in het Nederlands dat afkomstig is uit een chat. 
Haal er zoveel mogelijk persoonlijke informatie uit over de persoon waarover het gaat. 
Laat bij elk gevonden gegeven het woord 'kl' ervoor zetten zonder categorieën te noemen.

Voorbeelden van gegevens die je moet zoeken: naam, werk, bezigheden, uiterlijk, hobby’s, relatiestatus, kinderen, familie, seksuele voorkeuren, gezondheid, locatie, voertuigen.

Voorbeeld output:
kl Jessica
kl woont in Utrecht
kl werkt als kapster
"""

@app.route("/extract", methods=["POST"])
def extract_info():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Geen invoer ontvangen"}), 400

    text = data["text"]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        result = response.choices[0].message.content.strip()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
