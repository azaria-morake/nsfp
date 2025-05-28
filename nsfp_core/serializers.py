
from rest_framework import serializers
from .models import Team, TeamPhoto, TeamVideo, StaffMember, SquadMember, TeamNeeds
from .utils import validate_username, validate_team_name, normalize_identifier
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import pycountry



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

class TeamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['profile_picture', 'location', 'email']
        extra_kwargs = {
            'email': {'required': False},
            'profile_picture': {'required': False}
        }

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['new_password'])
        return data

class TeamPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPhoto
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class TeamVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamVideo
        fields = ['id', 'youtube_url', 'created_at']
        read_only_fields = ['id', 'created_at']


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = ['id', 'username', 'full_name', 'role', 'profile_picture']
        read_only_fields = ['id']
        extra_kwargs = {
            'profile_picture': {'required': False}
        }

    def validate_username(self, value):
        # Reuse team username validation
        validate_username(value)
        if StaffMember.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_role(self, value):
        if not value.strip():
            raise serializers.ValidationError("Role cannot be empty")
        return value

    def create(self, validated_data):
        # Get team from request context
        team = self.context['request'].user
        return StaffMember.objects.create(team=team, **validated_data)
    
    def update(self, instance, validated_data):
        # Handle profile picture update
        new_profile = validated_data.get('profile_picture')
        if new_profile and instance.profile_picture:
            # Delete old file before saving new one
            instance.profile_picture.delete(save=False)
        return super().update(instance, validated_data)

class SquadMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SquadMember
        exclude = ['team']
        read_only_fields = ['team_level']
        extra_kwargs = {
            'dob': {'format': '%d/%m/%Y'}
        }


    def validate_username(self, value):
        
        """System-wide uniqueness check with custom validation"""
        # Use the model validator explicitly
        from .validators import validate_squad_username
        validate_squad_username(value)

        if (Team.objects.filter(username=value).exists() or
            StaffMember.objects.filter(username=value).exists() or
            SquadMember.objects.filter(username=value).exists()):
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_citizenship(self, value):
        if not pycountry.countries.get(name=value):
            raise serializers.ValidationError("Invalid country name")
        return value


    def validate_dob(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value

    
    def validate(self, data):
        # Calculate team level for validation
        from .utils import calculate_team_level
        
        # For updates, use existing DOB if not provided in request
        dob = data.get('dob', self.instance.dob if self.instance else None)
        if not dob:
            raise serializers.ValidationError({"dob": "Date of birth is required"})
            
        team_level = calculate_team_level(dob)
        team = self.context['request'].user
        
        # Check jersey number uniqueness within team level
        jersey_number = data.get('jersey_number')
        if jersey_number is not None:
            qs = SquadMember.objects.filter(
                team=team,
                team_level=team_level,
                jersey_number=jersey_number
            )
            
            # Exclude current instance during updates
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
                
            if qs.exists():
                raise serializers.ValidationError({
                    "jersey_number": f"Jersey number {jersey_number} is already taken in {team_level} team level"
                })
        
        return data


class TeamNeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamNeeds
        fields = ['id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_content(self, value):
        if len(value) > 2000:
            raise serializers.ValidationError("Content cannot exceed 2000 characters")
        return value