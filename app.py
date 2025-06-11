from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Logboek AI-backend draait correct."

@app.route("/extract", methods=["POST"])
def extract_info():
    data = request.get_json()
    tekst = data.get("text", "")

    if not tekst:
        return jsonify({"error": "Geen tekst ontvangen."}), 400

    prompt = f"""
Haal de meest persoonlijke informatie uit deze tekst. Zet 'kl' voor elk gevonden feit. Laat categorieën weg. Ook slecht geschreven of informele tekst is toegestaan. 
Voorbeeld:
klJohn woont in Amsterdam
klHij is 34 jaar
klHij rijdt een blauwe BMW

Tekst:
{tekst}
    """

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Je bent een expert in het extraheren van persoonlijke informatie."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )

        resultaat = response.choices[0].message.content.strip()
        return jsonify({"result": resultaat})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
