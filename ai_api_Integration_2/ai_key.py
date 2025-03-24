# run pip install -r requirements.txt to install the required packages
# run python ai_key.py to run the program

# --- Imports ---
import google.generativeai as genai
import os
import tkinter as tk
from tkinter import scrolledtext
import requests  # Second API
from flask import Flask, request, jsonify  # For secured endpoint
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import threading
import sys

# --- System Info for Troubleshooting (Requirement 5) ---
print(sys.executable)
print(sys.version)
print(sys.path)

# --- API Key Configuration (Gemini AI) ---
api_key = "AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE"
genai.configure(api_key=api_key)

# --- Initialize the Gemini AI Model (Requirement 2) ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Flask App Setup for Secured API Endpoint (Requirement 4) ---
app = Flask(__name__)
auth = HTTPBasicAuth()

# Create basic auth credentials
users = {
    "admin": generate_password_hash("securepassword")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Secured API route using Gemini AI
@app.route("/generate", methods=["POST"])
@auth.login_required
def secure_generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        if not prompt:
            # Custom error message for missing prompt (Requirement 1)
            return jsonify({"error": "Prompt is required"}), 400

        # Generate content using Gemini
        response = model.generate_content(prompt)
        return jsonify({"generated_text": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start Flask server on separate thread
# Demonstrates a secure API endpoint (Requirement 4)
def run_flask():
    app.run(port=5000)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# --- Main Function for GUI + API Integration ---
def generate_content():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        # Custom error for empty input (Requirement 1)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: Input text is required")
        return

    try:
        # Call to a second API to get public IP (Requirement 3)
        ip_response = requests.get("https://api.ipify.org?format=json")

        # Check for successful response (Requirement 5)
        if ip_response.status_code != 200:
            raise Exception("Failed to retrieve IP info")
        ip_data = ip_response.json()

        # Call Gemini API (Requirement 2)
        response = model.generate_content(user_input)
        result = f"Your IP: {ip_data['ip']}\n\nGemini Response:\n{response.text}"

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    except requests.exceptions.RequestException as req_err:
        # Network-related error handling (Requirement 1 & 5)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Network Error: {str(req_err)}")

    except Exception as e:
        # Catch-all for unexpected exceptions (Requirement 1)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")

# --- GUI Setup (Requirement 5 for testing) ---
root = tk.Tk()
root.title("Gemini API GUI")

input_label = tk.Label(root, text="Enter your prompt:")
input_label.pack()
input_text = scrolledtext.ScrolledText(root, height=5, width=50)
input_text.pack()

generate_button = tk.Button(root, text="Generate", command=generate_content)
generate_button.pack()

output_label = tk.Label(root, text="Generated Response:")
output_label.pack()
output_text = scrolledtext.ScrolledText(root, height=10, width=50)
output_text.pack()

# Run the GUI
root.mainloop()
