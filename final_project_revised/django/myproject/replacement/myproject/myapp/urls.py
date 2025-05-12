from django.urls import path
from .views import home, generate_view

urlpatterns = [
    path("", home, name="home"),
    path("generate/", generate_view, name="generate"),
]
