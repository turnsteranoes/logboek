from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # Sta CORS toe voor frontend

client = OpenAI()  # OpenAI client initialiseren (API key via env variabele OPENAI_API_KEY)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""
Je krijgt een tekst over een persoon. Haal alleen deze informatie eruit:
- naam
- leeftijd
- familie/gezin (zoals kinderen, partner)
- woonplaats
- werk
- hobby's
- seksuele voorkeur
- relatiestatus
- woonsituatie
- huisdieren
- gezondheid
- wat die persoon gaat doen die dag of in de toekomst

Schrijf alles zo kort mogelijk in één zin, met komma's tussen, zonder extra uitleg, met als prefix 'kl '. Gebruik gewone Nederlandse woorden, en let op fouten.

Voorbeeld output:
kl Jan, 35 jaar, woont in Utrecht, werkt in supermarkt, 2 kids, hobby fietsen, hetero, getrouwd, woont in huurhuis, kat, gezond, gaat naar school

Tekst:
\"\"\"{text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150,
        )
        antwoord = response.choices[0].message.content.strip()
        return jsonify({"result": antwoord})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

