# -*- coding: utf-8 -*-
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import TeamRegistrationSerializer, UserSerializer
from .models import Team
from knox.settings import knox_settings


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