from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Uncomment when you're ready to use OpenAI
# import openai

@csrf_exempt
def home(request):
    return render(request, "myapp/index.html")

@csrf_exempt
def generate_page(request):
    history = request.session.get("chat_history", [])
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        model_choice = request.POST.get("model", "gemini-1.5-flash")
        file_data = request.FILES.get("file_input")
        response_text = ""

        if prompt:
            if model_choice.startswith("gemini"):
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                model = genai.GenerativeModel(model_choice)

                if file_data:
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        for chunk in file_data.chunks():
                            temp_file.write(chunk)
                        gemini_response = model.generate_content([
                            prompt,
                            {
                                "mime_type": file_data.content_type,
                                "data": open(temp_file.name, "rb").read()
                            }
                        ])
                else:
                    gemini_response = model.generate_content(prompt)

                response_text = gemini_response.text

            # Uncomment if you decide to use OpenAI
            # elif model_choice == "other-api":
            #     openai.api_key = os.getenv("OPENAI_API_KEY")
            #     result = openai.ChatCompletion.create(
            #         model="gpt-4",
            #         messages=[{"role": "user", "content": prompt}]
            #     )
            #     response_text = result.choices[0].message.content

        history.append({"prompt": prompt, "response": response_text})
        request.session["chat_history"] = history
        return render(request, "myapp/generate.html", {"response": response_text, "prompt": prompt})

    return render(request, "myapp/generate.html")

def chat_history(request):
    return render(request, "myapp/chat_history.html", {
        "history": request.session.get("chat_history", [])
    })

def login_page(request):
    return render(request, "myapp/login.html")

def signup_page(request):
    return render(request, "myapp/signup.html")

def feedback_page(request):
    return render(request, "myapp/feedback.html")
