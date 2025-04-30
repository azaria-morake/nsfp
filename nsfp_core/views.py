# nsfp_core/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TeamRegistrationSerializer, CustomTokenObtainPairSerializer, TeamTokenObtainPairSerializer, SquadMemberSerializer, StaffSerializer
from .models import SquadMember, Team, Staff

class TeamRegistrationView(generics.CreateAPIView):
    serializer_class = TeamRegistrationSerializer
    authentication_classes = []  # Allow unauthenticated access

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class TeamTokenObtainPairView(TokenObtainPairView):
    serializer_class = TeamTokenObtainPairSerializer


class StaffListCreateView(generics.ListCreateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Staff.objects.filter(team=self.request.user)

class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Staff.objects.filter(team=self.request.user)

class SquadListCreateView(generics.ListCreateAPIView):
    serializer_class = SquadMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SquadMember.objects.filter(team=self.request.user)

class SquadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SquadMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SquadMember.objects.filter(team=self.request.user)