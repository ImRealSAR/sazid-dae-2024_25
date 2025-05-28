from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import google.generativeai as genai
import openai
import os
from dotenv import load_dotenv
from datetime import datetime
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
    except:
        pass
    return {
        "ai_name": "Your AI",
        "tone": "neutral",
        "user_name": "User",
        "about": ""
    }

@csrf_exempt
def home(request):
    return render(request, "myapp/index.html")

@csrf_exempt
def generate_page(request):
    chat = []
    response_text = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        model_choice = request.POST.get("model", "gemini-1.5-flash")
        uid = request.POST.get("firebase_uid", "").strip()

        prefs = get_user_preferences(uid if uid else "guest_user")
        ai_name = prefs.get("ai_name", "Your AI")
        tone = prefs.get("tone", "neutral")
        user_name = prefs.get("user_name", "User")
        about_user = prefs.get("about", "")

        # 🔁 Load last 2 messages from Firestore
        chat_ref = db.collection("users").document(uid).collection("chat_history")
        docs = chat_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(2).stream()
        recent_context = list(reversed([doc.to_dict() for doc in docs]))

        context_str = "\n".join([
            f"{user_name}: {c['prompt']}\n{ai_name}: {c['response']}" for c in recent_context
        ])

        system_prompt = (
            f"You are {ai_name}, an AI who helps {user_name} (about: {about_user}) in a {tone} tone.\n\n"
            f"{context_str}\n{user_name}: {prompt}\n{ai_name}:"
        )

        try:
            if model_choice.startswith("gemini"):
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                model = genai.GenerativeModel("gemini-1.5-flash")
                reply = model.generate_content(system_prompt)
                response_text = reply.text
            elif model_choice.startswith("openai"):
                openai.api_key = os.getenv("OPENAI_API_KEY")
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": system_prompt}]
                )
                response_text = completion.choices[0].message["content"]
        except Exception as e:
            response_text = "⚠️ AI error: " + str(e)

        # ✅ Save new chat to Firestore
        chat_ref.add({
            "prompt": prompt,
            "response": response_text,
            "timestamp": datetime.utcnow()
        })

        chat = recent_context + [{"prompt": prompt, "response": response_text}]

    return render(request, "myapp/generate.html", {
        "chat": chat
    })

@csrf_exempt
def onboarding_page(request):
    if request.method == "POST":
        uid = request.POST.get("firebase_uid", "").strip()
        ai_name = request.POST.get("ai_name", "Your AI")
        tone = request.POST.get("tone", "neutral")
        user_name = request.POST.get("user_name", "User")
        about = request.POST.get("about", "")
        if uid:
            db.collection("users").document(uid).set({
                "ai_name": ai_name,
                "tone": tone,
                "user_name": user_name,
                "about": about
            }, merge=True)
        return redirect("generate")
    return render(request, "myapp/onboarding.html")

@csrf_exempt
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        try:
            reset_link = auth.generate_password_reset_link(email)
            send_mail("Password Reset", f"Click to reset: {reset_link}", settings.DEFAULT_FROM_EMAIL, [email])
            return render(request, "myapp/password_reset.html", {"message": "Reset email sent!"})
        except:
            return render(request, "myapp/password_reset.html", {"error": "Failed to send reset link."})
    return render(request, "myapp/password_reset.html")

def settings_page(request):
    return render(request, "myapp/account_settings.html")

def login_page(request):
    return render(request, "myapp/login.html")

def signup_page(request):
    return render(request, "myapp/signup.html")

def chat_history(request):
    return render(request, "myapp/chat_history.html", {
        "history": request.session.get("chat_history", [])
    })

def feedback_page(request):
    return render(request, "myapp/feedback.html")

def logout_view(request):
    request.session.flush()
    return redirect("home")
