from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json
import base64
import google.generativeai as genai

genai.configure(api_key="AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE")
model = genai.GenerativeModel("gemini-1.5-flash")

def home(request):
    return render(request, "myapp/index.html")

@csrf_exempt
def generate_view(request):
    if request.method == "POST":
        try:
            auth_header = request.headers.get("Authorization", "")
            auth_type, auth_info = auth_header.split(None, 1)
            if auth_type.lower() != 'basic':
                return JsonResponse({'error': 'Only Basic Auth supported'}, status=401)
            username, password = base64.b64decode(auth_info).decode().split(':', 1)
            if username != 'admin' or password != 'securepassword':
                return JsonResponse({'error': 'Invalid credentials'}, status=403)

            data = json.loads(request.body)
            prompt = data.get("prompt", "")
            if not prompt:
                return JsonResponse({'error': 'Prompt required'}, status=400)
            response = model.generate_content(prompt)
            return JsonResponse({'generated_text': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'POST method required'}, status=405)
