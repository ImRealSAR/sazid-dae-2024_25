from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate-ai/', views.generate_page, name='generate'),
    path('chat-history/', views.chat_history, name='chat_history'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('onboarding/', views.onboarding_page, name='onboarding'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('account/', views.settings_page, name='settings'),
    path('logout/', views.logout_view, name='logout'),
]
