from django.urls import path
from .views import home, generate_view

urlpatterns = [
    path("", home, name="home"),
    # path("generate-ai/", generate_page, name="generate-page"),  # Removed because generate_page does not exist
    path("generate/", generate_view, name="generate"),
]
# The above code defines the URL patterns for the Django application.