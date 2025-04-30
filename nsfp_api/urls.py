# nsfp_api/urls.py
from django.urls import path

"""
nsfp_api URL Configuration
The `urlpatterns` list routes URLs to views. 

"""

from nsfp_core.views import (
    StaffListCreateView, StaffDetailView,
    SquadListCreateView, SquadDetailView,
    TeamRegistrationView, CustomTokenObtainPairView,
    TeamTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings

urlpatterns = [
    path('api/register/', TeamRegistrationView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     # Staff Endpoints
    path('api/staff/', StaffListCreateView.as_view(), name='staff-list'),
    path('api/staff/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    
    # Squad Endpoints
    path('api/squad/', SquadListCreateView.as_view(), name='squad-list'),
    path('api/squad/<int:pk>/', SquadDetailView.as_view(), name='squad-detail'),
]