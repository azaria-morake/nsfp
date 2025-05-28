# core/models.py
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CITextField
from .utils import validate_username, validate_team_name, normalize_identifier
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
import os
from .validators import validate_image_size, validate_squad_username
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from django.db import models
import pycountry
from datetime import date


def staff_profile_picture_path(instance, filename):
    
    """
    Generates a file path for a staff member's profile picture.

    Args:
        instance: An instance of the StaffMember model.
        filename: The name of the file to be saved.

    Returns:
        A string representing the file path where the staff member's 
        profile picture will be stored, formatted as: 
        "<team_name>/staff/<username>/<filename>".
    """

    return f"{instance.team.team_name.replace(' ', '_')}/staff/{instance.username}/{filename}"


def profile_picture_path(instance, filename):
    return f"{instance.team_name.replace(' ', '_')}/profile/{filename}"

def player_picture_path(instance, filename):
    return f"{instance.team.team_name.replace(' ', '_')}/squad/{instance.username}/{filename}"
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
            validate_image_size
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('team', 'username')

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class SquadMember(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('LB', 'Left Back'),
        ('RB', 'Right Back'),
        ('CDM', 'Defensive Midfielder'),
        ('CM', 'Central Midfielder'),
        ('CAM', 'Attacking Midfielder'),
        ('LW', 'Left Winger'),
        ('RW', 'Right Winger'),
        ('ST', 'Striker'),
    ]
    
    FOOT_CHOICES = [
        ('L', 'Left'),
        ('R', 'Right'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='squad_members')
    username = models.CharField(
        max_length=30, 
        unique=True,
        validators=[validate_squad_username] 
        )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField()
    citizenship = models.CharField(max_length=100)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    strong_foot = models.CharField(max_length=1, choices=FOOT_CHOICES)
    jersey_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    nickname = models.CharField(max_length=50, blank=True, null=True)
    team_level = models.CharField(max_length=3, editable=False)
    profile_picture = models.ImageField(
        upload_to=player_picture_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size
        ]
    )
    market_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('team', 'jersey_number')]
        ordering = ['jersey_number']

    def clean(self):
        # Date validation
        print("Clean method called!")  # Debug line
        if self.dob > date.today():
            raise ValidationError({'dob': 'Date of birth cannot be in the future'})
        
        # Citizenship validation
        if not pycountry.countries.get(name=self.citizenship):
            raise ValidationError({'citizenship': 'Invalid country name'})

    def save(self, *args, **kwargs):
        # Calculate team level
        today = date.today()
        cutoff_date = date(today.year, 1, 1)
        age = cutoff_date.year - self.dob.year - (
            (cutoff_date.month, cutoff_date.day) < (self.dob.month, self.dob.day)
        )
        
        if age <= 13: self.team_level = 'U13'
        elif age <= 15: self.team_level = 'U15'
        elif age <= 19: self.team_level = 'U19'
        elif age <= 21: self.team_level = 'U21'
        else: self.team_level = 'SR'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"
    

@receiver(pre_save, sender=SquadMember)
def delete_old_squad_picture(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = SquadMember.objects.get(pk=instance.pk)
    except SquadMember.DoesNotExist:
        return

    old_file = old_instance.profile_picture
    new_file = instance.profile_picture

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)