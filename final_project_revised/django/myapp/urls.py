from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate-ai/', views.generate_page, name='generate'),
    path('chat-history/', views.chat_history, name='chat_history'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),  # ✅ This ensures the route works
]

# This code defines the URL patterns for a Django application. It maps different URL paths to their corresponding view functions, allowing users to access various pages of the application. The urlpatterns list includes paths for the home page, AI generation page, chat history page, feedback page, login page, and signup page. Each path is associated with a specific view function that handles the request and response for that URL.