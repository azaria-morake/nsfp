# -*- coding: utf-8 -*-
import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_username(value):
    """Instagram-like username validation"""
    if not re.match(r'^[a-zA-Z0-9._]{4,30}$', value):
        raise ValidationError(
            "Username must be 4-30 characters with letters, numbers, . or _"
        )

class Team(AbstractUser):
    team_name = models.CharField(
        max_length=100,
        unique=True,
        error_messages={'unique': 'This team name is already registered'}
    )
    location = models.CharField(max_length=200)
    
    # Remove first_name/last_name fields from AbstractUser
    first_name = None
    last_name = None
    
    # Override username field with custom validation
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[validate_username],
        error_messages={'unique': 'Username already taken'}
    )

    def __str__(self):
        return f"{self.team_name} ({self.username})"