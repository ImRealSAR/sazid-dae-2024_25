from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    return render(request, "myapp/index.html")

@csrf_exempt
def generate_page(request):
    import google.generativeai as genai
    import openai

    history = request.session.get("chat_history", [])
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        selected_model = request.POST.get("model", "gemini-1.5-flash")

        if prompt:
            if selected_model.startswith("gemini"):
                genai.configure(api_key="YOUR_GEMINI_API_KEY")
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(prompt)
                text = response.text
            elif selected_model == "other-api":
                openai.api_key = "YOUR_OPENAI_API_KEY"
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                text = completion.choices[0].message.content
            else:
                text = "Unsupported model selected."

            history.append({"prompt": prompt, "response": text})
            request.session["chat_history"] = history
            return render(request, "myapp/generate.html", {"response": text, "prompt": prompt})
    return render(request, "myapp/generate.html")

def chat_history(request):
    history = request.session.get("chat_history", [])
    return render(request, "myapp/chat_history.html", {"history": history})

def login_page(request):
    return render(request, "myapp/login.html")

def signup_page(request):
    return render(request, "myapp/signup.html")

def feedback_page(request):
    return render(request, "myapp/feedback.html")
