"""marketplace_app.info URL Configuration
"""
from django.urls import path
from .views import AboutView

app_name = 'info'

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
]
