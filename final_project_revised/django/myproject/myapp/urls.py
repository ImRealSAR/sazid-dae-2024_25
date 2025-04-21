from django.urls import path
from .views import home, generate_view

urlpatterns = [
    path("", home),
    path("generate/", generate_view, name="generate"),
]
