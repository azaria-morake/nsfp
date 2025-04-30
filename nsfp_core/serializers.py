# nsfp_core/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Team, Staff, BaseMember, SquadMember
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, validate_email
from rest_framework.validators import UniqueValidator
from datetime import date


class TeamRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Team.objects.all(),
                message="This email is already registered."
            )
        ]
    )

    class Meta:
        model = Team
        fields = ['username', 'password', 'team_name', 'location', 'email']
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def validate_email(self, value):
        # Validate email format using Django's built-in validator
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        
        return value

    def create(self, validated_data):
        # Create Team (user) with validated data
        team = Team.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            team_name=validated_data['team_name'],
            location=validated_data['location'],
            email=validated_data['email']
        )
        return team

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Safely get team name (avoid RelatedObjectDoesNotExist)
        try:
            token['team_name'] = user.team_name
        except Team.DoesNotExist:
            token['team_name'] = None  # Or omit this key entirely
        
        return token


class TeamTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, team):
        token = super().get_token(team)
        # Add team-specific claims
        token['team_name'] = team.team_name
        return token

from rest_framework import serializers
from .models import BaseMember, Staff, SquadMember, Team

class StaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    # Add read-only username field from BaseMember
    member_username = serializers.CharField(source='base_member.username', read_only=True)

    class Meta:
        model = Staff
        fields = [
            'member_username',  # Read-only username from BaseMember
            'username',         # Write-only during creation
            'team_name',        # Team name instead of ID
            'full_name', 
            'role', 
            'profile_picture'
        ]
        read_only_fields = ['team_name']

    def validate_username(self, value):
        if BaseMember.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user  # Team admin
        username = validated_data.pop('username')
        
        base_member = BaseMember.objects.create(username=username)
        staff = Staff.objects.create(
            base_member=base_member,
            team=user,
            **validated_data
        )
        return staff

class SquadMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    member_username = serializers.CharField(source='base_member.username', read_only=True)

    class Meta:
        model = SquadMember
        fields = [
            'member_username',
            'username',
            'team_name',
            'full_name', 
            'dob', 
            'citizenship',
            'position', 
            'strong_foot', 
            'jersey_number', 
            'nickname',
            'profile_picture', 
            'market_value', 
            'team_level'
        ]

    def validate_username(self, value):
        if BaseMember.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_dob(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user  # Team admin
        username = validated_data.pop('username')
        
        base_member = BaseMember.objects.create(username=username)
        squad_member = SquadMember.objects.create(
            base_member=base_member,
            team=user,
            **validated_data
        )
        return squad_member