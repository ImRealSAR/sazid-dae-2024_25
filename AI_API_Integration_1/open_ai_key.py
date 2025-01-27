import google.generativeai as genai
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configure the API
api_key = "AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE"
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        # Extract the user input from the request body
        user_input = request.json.get('input', '')
        
        if not user_input:
            return jsonify({"error": "Input text is required"}), 400

        # Generate content using Gemini
        response = model.generate_content(user_input)
        return jsonify({"generated_text": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    return jsonify({"status": "API is working", "model": "gemini-1.5-flash"})

if __name__ == '__main__':
    app.run(debug=True)
