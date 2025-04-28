
from django.urls import path
from .views import home, generate_page, generate_view

urlpatterns = [
    path("", home, name="home"),
    path("generate-ai/", generate_page, name="generate-page"),
    path("generate/", generate_view, name="generate"),
]
