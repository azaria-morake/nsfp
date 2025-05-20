# -*- coding: utf-8 -*-
from rest_framework import serializers
from nsfp_core.models import Team

class TeamRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = Team
        fields = ['username', 'team_name', 'password', 'password2', 'location']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError("Passwords do not match")
        
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        
        return data

    def create(self, validated_data):
        user = Team.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            team_name=validated_data['team_name'],
            location=validated_data['location']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['username', 'team_name', 'location']