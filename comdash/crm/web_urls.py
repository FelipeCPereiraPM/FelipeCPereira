from django.urls import path
from .web_views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
]