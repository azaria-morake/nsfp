# nsfp_api/urls.py
from django.urls import path
from nsfp_core.views import health_check

urlpatterns = [
    path('api/health/', health_check),
]