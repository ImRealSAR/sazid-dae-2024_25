from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import google.generativeai as genai
import openai
import os
from dotenv import load_dotenv
load_dotenv()

import firebase_admin
from firebase_admin import credentials, firestore, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user_preferences(uid):
    try:
        doc = db.collection("users").document(uid).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print("Error fetching preferences:", e)
    return {
        "ai_name": "Your AI",
        "tone": "neutral",
        "user_name": "User",
        "about": "a curious thinker"
    }


@csrf_exempt
def home(request):
    return render(request, "myapp/index.html")


@csrf_exempt
def generate_page(request):
    response_text = ""
    prompt = request.POST.get("prompt", "")
    uid = request.POST.get("firebase_uid", "guest_user").strip()
    model_choice = request.POST.get("model", "gemini-1.5-flash")

    prefs = get_user_preferences(uid)
    ai_name = prefs.get("ai_name", "Your AI")
    tone = prefs.get("tone", "neutral")
    user_name = prefs.get("user_name", "User")
    about = prefs.get("about", "a curious thinker")

    mentor_prompt = f"""
You are an AI mentor named {ai_name}.
Speak in a {tone} tone.
You are guiding {user_name}, who is {about}.
Make your responses thoughtful, friendly, and personal.
Avoid giving answers directly — instead guide with insights.
"""

    # Load recent history (limit to 3)
    context_messages = []
    if uid != "guest_user":
        try:
            chats = db.collection("users").document(uid).collection("chat_history").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(3).stream()
            for chat in reversed(list(chats)):
                data = chat.to_dict()
                context_messages.append({"role": "user", "content": data.get("prompt", "")})
                context_messages.append({"role": "assistant", "content": data.get("response", "")})
        except:
            pass

    # Add current prompt to conversation
    context_messages.append({"role": "user", "content": prompt})

    if model_choice.startswith("gemini"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        gemini_response = model.generate_content([
            mentor_prompt,
            prompt
        ])
        response_text = gemini_response.text

    elif model_choice.startswith("openai"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": mentor_prompt}
            ] + context_messages
        )
        response_text = chat_response.choices[0].message['content']

    # Save conversation
    if uid != "guest_user":
        db.collection("users").document(uid).collection("chat_history").add({
            "prompt": prompt,
            "response": response_text,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

    return render(request, "myapp/generate.html", {
        "response": response_text,
        "prompt": prompt
    })


@csrf_exempt
def onboarding_page(request):
    if request.method == "POST":
        uid = request.POST.get("firebase_uid", "").strip()
        ai_name = request.POST.get("ai_name", "Your AI")
        tone = request.POST.get("tone", "neutral")
        user_name = request.POST.get("user_name", "User")
        about = request.POST.get("about", "a curious thinker")
        if uid:
            db.collection("users").document(uid).set({
                "ai_name": ai_name,
                "tone": tone,
                "user_name": user_name,
                "about": about
            }, merge=True)
        return redirect("generate")
    return render(request, "myapp/onboarding.html")
