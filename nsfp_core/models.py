# core/models.py
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CITextField
from .utils import validate_username, validate_team_name, normalize_identifier

def validate_username(value):
    """Instagram-like username validation"""
    if not re.match(r'^[a-zA-Z0-9._]{4,30}$', value):
        raise ValidationError(
            "Username must be 4-30 characters with letters, numbers, . or _"
        )

class Team(AbstractUser):
    team_name = models.CharField(
        max_length=100,
        unique=False,  # Canonical version enforces uniqueness
        validators=[validate_team_name],
        error_messages={'unique': 'This team name is already registered'}
    )
    location = models.CharField(max_length=200)

    # Canonical fields (case-insensitive, ICU-aware collation)
    canonical_username = models.TextField(
        max_length=100,
        unique=True,
        editable=False,
        db_index=True,
        db_collation='und-x-icu'
    )
    canonical_team_name = models.TextField(
        max_length=100,
        unique=True,
        editable=False,
        db_index=True,
        db_collation='und-x-icu'
    )

    # Remove unnecessary name fields
    first_name = None
    last_name = None

    # Custom username with validation
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[validate_username],
        error_messages={'unique': 'Username already taken'}
    )

    def save(self, *args, **kwargs):
        # Normalize both team name and username before saving
        self.canonical_team_name = normalize_identifier(self.team_name)
        self.canonical_username = normalize_identifier(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_name} ({self.username})"
