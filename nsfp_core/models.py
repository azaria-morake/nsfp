# core/models.py
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CITextField
from .utils import validate_username, validate_team_name, normalize_identifier
from django.core.validators import FileExtensionValidator, MaxValueValidator
import os
from .validators import validate_image_size
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save


def staff_profile_picture_path(instance, filename):
    return f"{instance.team.team_name.replace(' ', '_')}/staff/{instance.username}/{filename}"


def profile_picture_path(instance, filename):
    return f"{instance.team_name.replace(' ', '_')}/profile/{filename}"

def team_photo_path(instance, filename):
    return f"{instance.team.team_name.replace(' ', '_')}/photos/{filename}"

def team_media_path(instance, filename):
    # Generates paths like: "Golden_Lions_FC/images/profile_picture.jpg"
    return f"{instance.team_name.replace(' ', '_')}/{instance.media_type}/{filename}"

def validate_username(value):
    """Instagram-like username validation"""
    if not re.match(r'^[a-zA-Z0-9._]{4,30}$', value):
        raise ValidationError(
            "Username must be 4-30 characters with letters, numbers, . or _"
        )


class Team(AbstractUser):
    # Custom fields
    team_name = models.CharField(
        max_length=100,
        unique=False,  # Canonical version enforces uniqueness
        validators=[validate_team_name],
        error_messages={'unique': 'This team name is already registered'}
    )
    location = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    profile_picture = models.ImageField(
        upload_to=profile_picture_path,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size
        ]
    )

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

    @property
    def media_type(self):
        return "profile"


class TeamPhoto(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(
        upload_to=team_photo_path, 
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'image')
        ordering = ['-uploaded_at']

class TeamVideo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='videos')
    youtube_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if "youtube.com" not in self.youtube_url and "youtu.be" not in self.youtube_url:
            raise ValidationError("Only YouTube URLs are allowed")

    class Meta:
        ordering = ['-created_at']

@receiver(pre_save, sender=TeamPhoto)
def delete_old_team_photo_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = TeamPhoto.objects.get(pk=instance.pk)
    except TeamPhoto.DoesNotExist:
        return

    old_file = old_instance.image
    new_file = instance.image

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class StaffMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='staff')
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[validate_username]
    )
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    profile_picture = models.ImageField(
        upload_to=staff_profile_picture_path,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            MaxValueValidator(2*1024*1024, message="Image size cannot exceed 2MB")
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('team', 'username')

    def __str__(self):
        return f"{self.full_name} ({self.role})"
