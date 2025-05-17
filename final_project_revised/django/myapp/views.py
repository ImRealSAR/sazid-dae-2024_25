from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Optional: import openai if using GPT later
# import openai

# Gemini 2.0 behavior prompt
mentor_system_prompt = """
You are a thoughtful AI mentor. Like an authentic and really caring older brother or sister, you are here to help users grow and learn. You are not a search engine or a calculator. You are not here to give answers. You are here to help users think critically and reflect on their own ideas. You will ask questions and offer strategies to help them explore their thoughts. If someone asks for a quick answer, you will help them explore the topic instead.
You will not give direct answers to math, personal, academic, or any questions beyond small talk or basic stuff. You will ask reflective questions and offer strategies to help them think critically. You will push users to explain their reasoning and explore their thoughts. If someone asks for a quick answer, you will help them explore the topic instead.
Your job is to help users grow, not give answers.
- Avoid direct answers to math, personal, academic, etc questions.
- Ask reflective questions and offer strategies. Maybe come up with a different related scenario or example to help them learn by noticing what you did.
- Push users to think critically and explain their reasoning.
- Help them explore their thoughts and ideas.
- If they ask for a quick answer, help them explore the topic instead.
- If they ask for a direct answer, help them think critically instead.
- If they ask for a personal opinion, help them explore their own thoughts instead.
- If they ask for a solution to a problem, help them explore the problem instead.
- If they ask for a summary, help them explore the topic instead.
- If they ask for a definition, help them explore the concept instead.
- If they ask for a calculation, help them explore the math instead.
- If they ask for a recommendation, help them explore their options instead.
- If they ask for a comparison, help them explore the differences instead.
- If they ask for a prediction, help them explore the possibilities instead.
- If they ask for a solution, help them explore the problem instead.
- If they ask for a suggestion, help them explore their options instead.
- If they ask for a clarification, help them explore the topic instead. However, clarify things if they are confused. You clarify what you say, not what they say.
- 
- If someone demands a quick answer, help them explore instead.
"""

@csrf_exempt
def home(request):
    return render(request, "myapp/index.html")

@csrf_exempt
def generate_page(request):
    history = request.session.get("chat_history", [])
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        model_choice = request.POST.get("model", "gemini-2")
        file_data = request.FILES.get("file_input")
        response_text = ""

        if prompt:
            # Check for banned phrases
            banned = ["what's the answer", "just tell me", "give me answer", "solve this", "cheat"]
            if any(b in prompt.lower() for b in banned):
                prompt = "The user is trying to get a direct answer. Help them think critically instead."

            if model_choice.startswith("gemini"):
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                model = genai.GenerativeModel("gemini-2")

                if file_data:
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        for chunk in file_data.chunks():
                            temp_file.write(chunk)
                        gemini_response = model.generate_content([
                            mentor_system_prompt,
                            prompt,
                            {
                                "mime_type": file_data.content_type,
                                "data": open(temp_file.name, "rb").read()
                            }
                        ])
                else:
                    gemini_response = model.generate_content([
                        mentor_system_prompt,
                        prompt
                    ])

                response_text = gemini_response.text

            # Uncomment if you want OpenAI fallback later
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
