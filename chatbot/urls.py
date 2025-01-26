# chatbot/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.ai_response_view, name="chatbot"),
]