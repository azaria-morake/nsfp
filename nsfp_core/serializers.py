
from rest_framework import serializers
from .models import Team
from .utils import validate_username, validate_team_name, normalize_identifier
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



class TeamRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = Team
        fields = ['username', 'team_name', 'password', 'password2', 'location']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'validators': [validate_username]},
            'team_name': {'validators': [validate_team_name]}
        }

    def validate(self, data):
        # Normalize both identifiers the same way
        base_username = normalize_identifier(data['username'])
        base_team_name = normalize_identifier(data['team_name'])

                # Password validation
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        
        # Check against existing records
        if Team.objects.filter(canonical_username=base_username).exists():
            raise serializers.ValidationError({
                "username": "This username is already taken (including FC/CF variations)"
            })
        
        if Team.objects.filter(canonical_team_name=base_team_name).exists():
            raise serializers.ValidationError({
                "team_name": "This team name is already taken (including FC/CF variations)"
            })
        
        # Store normalized versions
        data['canonical_username'] = base_username
        data['canonical_team_name'] = base_team_name
        
        return data

    def create(self, validated_data):
        user = Team.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            team_name=validated_data['team_name'],
            location=validated_data['location'],
            canonical_username=validated_data['canonical_username'],
            canonical_team_name=validated_data['canonical_team_name']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['username', 'team_name', 'location']