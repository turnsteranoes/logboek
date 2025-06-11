from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Logboek API is live!"

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    text = data.get('text', '')
    # Hier kun je je AI verwerking doen, voor nu geven we alleen terug met 'kl ' prefix
    result = f"kl {text}"
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
