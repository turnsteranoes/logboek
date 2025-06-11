from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_personal_info_short(text):
    prompt = f"""
    Lees onderstaande tekst en haal alleen de volgende persoonlijke info eruit: 
    naam, leeftijd, werk, gezin (zoals kinderen en familie), woonplaats, hobby's, 
    gezondheid, relatie status, woonsituatie, huisdieren, seksuele voorkeuren, en 
    wat de persoon gaat doen vandaag of in de toekomst.

    Geef dit kort en bondig in één regel, zonder hele zinnen. Gebruik alleen woorden, 
    scheid met komma's, en begin met 'kl '.

    Tekst:
    {text}

    Voorbeeld output:
    kl jan, 35 jaar, werkt in supermarkt, 2 kids, vrouw, woont amsterdam, hobby gitaar, gezond, hetero, single, huis met tuin, hond, gaat naar feestje
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Je bent een info-extractor die persoonlijke info kort samenvat."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"kl fout bij verwerken: {str(e)}"

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'result': 'kl geen tekst ontvangen'}), 400
    result = extract_personal_info_short(text)
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
