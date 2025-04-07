# run pip install -r requirements.txt to make sure all dependencies met
# ai_key.py

import os
import sys
import threading
import tkinter as tk
from tkinter import scrolledtext
import requests
import base64
import google.generativeai as genai

# --- Django Setup ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gemini_django.settings')
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure Django settings manually
if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        SECRET_KEY="insecure-key",
        MIDDLEWARE=[],
        INSTALLED_APPS=[],
    )
    django.setup()

# --- Gemini API Configuration ---
api_key = "AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Django View for /generate Endpoint ---
@method_decorator(csrf_exempt, name='dispatch')
class GenerateView(View):
    def post(self, request):
        if "HTTP_AUTHORIZATION" not in request.META:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            auth_type, auth_info = request.META['HTTP_AUTHORIZATION'].split(None, 1)
            if auth_type.lower() != 'basic':
                return JsonResponse({'error': 'Only Basic Auth is supported'}, status=401)
            username, password = base64.b64decode(auth_info).decode().split(':', 1)
            if username != 'admin' or password != 'securepassword':
                return JsonResponse({'error': 'Invalid credentials'}, status=403)

            import json
            data = json.loads(request.body.decode('utf-8'))
            prompt = data.get('prompt', '')
            if not prompt:
                return JsonResponse({'error': 'Prompt is required'}, status=400)

            response = model.generate_content(prompt)
            return JsonResponse({'generated_text': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# --- Django URL Configuration ---
urlpatterns = [
    path("generate/", GenerateView.as_view(), name="generate")
]

# --- Run Django Server in Thread ---
def run_django():
    from django.core.servers.basehttp import run
    application = get_wsgi_application()
    run("127.0.0.1", 8000, application)

django_thread = threading.Thread(target=run_django, daemon=True)
django_thread.start()

# --- GUI Functionality (Tkinter) ---
def generate_content():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: Input text is required")
        return

    try:
        # Get IP Address
        ip_response = requests.get("https://api.ipify.org?format=json")
        if ip_response.status_code != 200:
            raise Exception("Failed to retrieve IP info")
        ip_data = ip_response.json()

        # Make secure POST request to Django endpoint
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(b'admin:securepassword').decode('utf-8')
        }
        response = requests.post("http://127.0.0.1:8000/generate/", headers=headers, json={"prompt": user_input})
        result_json = response.json()

        if response.status_code == 200:
            result = f"Your IP: {ip_data['ip']}

Gemini Response:
{result_json['generated_text']}"
        else:
            result = f"Error: {result_json.get('error', 'Unknown error')}"

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    except requests.exceptions.RequestException as req_err:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Network Error: {str(req_err)}")
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")

# --- GUI Setup ---
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

# --- Run GUI Loop ---
root.mainloop()
