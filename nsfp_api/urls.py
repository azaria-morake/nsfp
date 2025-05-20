from django.urls import path
from nsfp_core.views import (
    TeamRegistrationView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    TeamDetailView,
    ActiveSessionsView
)

"""
nsfp_api URL Configuration
The `urlpatterns` list routes URLs to views. 

"""
# Import the necessary views from nsfp_core.views
urlpatterns = [
    path('api/register/', TeamRegistrationView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('api/teams/me/', TeamDetailView.as_view(), name='team-detail'),
    path('api/sessions/', ActiveSessionsView.as_view(), name='active-sessions'),
]