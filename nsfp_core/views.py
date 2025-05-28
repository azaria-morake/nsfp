# -*- coding: utf-8 -*-
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import (
        TeamRegistrationSerializer, 
        UserSerializer, 
        TeamProfileSerializer, 
        PasswordChangeSerializer, 
        TeamPhotoSerializer, 
        TeamVideoSerializer, 
        StaffSerializer,
        SquadMemberSerializer,
        TeamNeedsSerializer
        )

from .models import Team, TeamPhoto, TeamVideo, StaffMember, SquadMember, TeamNeeds

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from knox.settings import knox_settings
from rest_framework.permissions import IsAuthenticated
import logging
# Initialize logger
logger = logging.getLogger(__name__)
# This module contains views for team registration, login, logout, and profile management.
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import serializers


# Views for team registration, login, logout, and profile management

class TeamRegistrationView(generics.GenericAPIView):
    serializer_class = TeamRegistrationSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        # Validate credentials
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = Team.objects.get(username=username)
            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=401)
        except Team.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        # Enforce active session limit (max 3 tokens)
        active_tokens = AuthToken.objects.filter(user=user)
        if active_tokens.count() >= 3:
            return Response(
                {"error": "Maximum 3 active sessions allowed. Please log out from another device."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new token
        token = AuthToken.objects.create(user)

        return Response({
            "user": UserSerializer(user).data,
            "token": token[1]
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        request._auth.delete()  # Delete Knox token
        return Response({"message": "Successfully logged out"})

# Refresh token view
class RefreshTokenView(generics.GenericAPIView):
    """
    Refresh authentication token. 
    Deletes the current token and issues a new one.
    Requires valid authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Delete the current token
        request.auth.delete()  # Knox attaches the token to request.auth
        
        # Create new token
        new_token = AuthToken.objects.create(request.user)
        
        return Response({
            "token": new_token[1],  # Token string is the second element
            "expiry": new_token[0].expiry  # Optional: Return token expiry time
        })


# Temporary view for testing
class TestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
# This view is for testing purposes only and should be removed in production.

class TeamDetailView(generics.RetrieveAPIView):
    """Temporary view for testing authentication-protected endpoints"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user  # Returns the authenticated team's data
    # This view is for testing purposes only and should be removed in production.

# View to list and revoke active sessions
class ActiveSessionsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        tokens = AuthToken.objects.filter(user=request.user).values_list('created', 'expiry')
        return Response({
            "active_sessions": [
                {"created": token[0], "expires": token[1]} for token in tokens
            ]
        })
    
    def delete(self, request):
        token_key = request.data.get('token_key')  # Partial token to revoke (first 8 chars)
        if not token_key:
            return Response({"error": "Specify 'token_key' to revoke"}, status=400)
        
        AuthToken.objects.filter(
            user=request.user,
            token_key__startswith=token_key
        ).delete()
        return Response({"message": "Session revoked"})

class TeamProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = TeamProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Check for no changes
        if not request.data:
            return Response({"detail": "No changes detected"}, status=status.HTTP_400_BAD_REQUEST)
            
        return super().update(request, *args, **kwargs)

class PasswordChangeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.data['old_password']):
            return Response({"old_password": "Incorrect password"}, status=400)
        
        user.set_password(serializer.data['new_password'])
        user.save()
        
        # Create new token and delete old one
        AuthToken.objects.filter(user=user).delete()
        token = AuthToken.objects.create(user)
        
        return Response({
            "detail": "Password updated successfully",
            "token": token[1]
        })

class TeamPhotoListView(generics.ListCreateAPIView):
    serializer_class = TeamPhotoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser] 

    def get_queryset(self):
        return TeamPhoto.objects.filter(team=self.request.user)

    def perform_create(self, serializer):
        # Enforce 10 photo limit
        if self.request.user.photos.count() >= 10:
            raise serializers.ValidationError("Maximum 10 photos allowed per team")
        serializer.save(team=self.request.user)

class TeamPhotoDetailView(generics.DestroyAPIView):
    queryset = TeamPhoto.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.team != self.request.user:
            self.permission_denied(self.request)
        return obj

class TeamVideoListView(generics.ListCreateAPIView):
    serializer_class = TeamVideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamVideo.objects.filter(team=self.request.user)

    def perform_create(self, serializer):
        serializer.save(team=self.request.user)

class TeamVideoDetailView(generics.DestroyAPIView):
    queryset = TeamVideo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.team != self.request.user:
            self.permission_denied(self.request)
        return obj
    
class StaffListView(generics.ListCreateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StaffMember.objects.filter(team=self.request.user)


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StaffMember.objects.filter(team=self.request.user)
    
    def perform_update(self, serializer):
        # Prevent username changes
        if 'username' in serializer.validated_data:
            current_user = StaffMember.objects.get(pk=serializer.instance.pk)
            if serializer.validated_data['username'] != current_user.username:
                raise serializers.ValidationError({"username": "Username cannot be changed"})
        
        serializer.save()

class SquadMemberListView(generics.ListCreateAPIView):
    serializer_class = SquadMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['team_level', 'position']
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return SquadMember.objects.filter(team=self.request.user)

    def perform_create(self, serializer):
        serializer.save(team=self.request.user)

class SquadMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SquadMemberSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def get_queryset(self):
        return SquadMember.objects.filter(team=self.request.user)

    def perform_update(self, serializer):
        # Prevent DOB changes
        if 'dob' in serializer.validated_data:
            if serializer.validated_data['dob'] != serializer.instance.dob:
                raise serializers.ValidationError({"dob": "Date of birth cannot be changed"})
        serializer.save()

class TeamNeedsListView(generics.ListCreateAPIView):
    serializer_class = TeamNeedsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamNeeds.objects.filter(team=self.request.user)

    def perform_create(self, serializer):
        serializer.save(team=self.request.user)

class TeamNeedsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamNeedsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamNeeds.objects.filter(team=self.request.user)