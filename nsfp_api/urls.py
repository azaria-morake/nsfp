from django.urls import path
from nsfp_core.views import (
    TeamRegistrationView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    TeamDetailView,
    ActiveSessionsView,
    TeamProfileView,
    PasswordChangeView,
    TeamPhotoListView,
    TeamPhotoDetailView,
    TeamVideoListView,
    TeamVideoDetailView,
    StaffListView,
    StaffDetailView,
    SquadMemberListView,
    SquadMemberDetailView
)
from django.conf.urls.static import static
from django.conf import settings

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
    
    # Profile Management
    path('api/profile/', TeamProfileView.as_view(), name='team-profile'),
    path('api/change-password/', PasswordChangeView.as_view(), name='change-password'),
    
    # Media Management
    path('api/photos/', TeamPhotoListView.as_view(), name='team-photos'),
    path('api/photos/<int:pk>/', TeamPhotoDetailView.as_view(), name='team-photo-detail'),
    path('api/videos/', TeamVideoListView.as_view(), name='team-videos'),
    path('api/videos/<int:pk>/', TeamVideoDetailView.as_view(), name='team-video-detail'),
    path('api/staff/', StaffListView.as_view(), name='staff-list'),
    path('api/staff/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    path('api/squad/', SquadMemberListView.as_view(), name='squad-list'),
    path('api/squad/<int:pk>/', SquadMemberDetailView.as_view(), name='squad-detail'),    
                ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development

# Note: In production, you should configure your web server to serve media files.
# This is typically done with a web server like Nginx or Apache, not Django.
# This is a simple URL configuration for the NSFP API.
# It includes paths for team registration, login, logout, token refresh,
# team detail, active sessions, profile management, and media management.
#