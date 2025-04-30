# nsfp_core/models.py


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date
import pycountry

class Team(AbstractUser):
    # Inherits username, password, email, etc. from AbstractUser
    team_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,  # Enforce global uniqueness
        validators=[
            EmailValidator(
                message="Enter a valid email address (e.g., team@example.com).",
                code="invalid_email"
            )
        ]
    )
    profile_picture = models.ImageField(
        upload_to='team_profile_pics/',
        validators=[FileExtensionValidator(['jpg', 'png'])],
        blank=True
    )

    def __str__(self):
        return self.team_name

class BaseMember(models.Model):
    username = models.CharField(max_length=100, unique=True)  # Enforce system-wide uniqueness
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = False  # Concrete base model

    def __str__(self):
        return self.username


# Staff Model
class Staff(models.Model):
    ROLE_CHOICES = [
        ('Coach', 'Coach'),
        ('Assistant Coach', 'Assistant Coach'),
        ('Physiotherapist', 'Physiotherapist'),
    ]

    base_member = models.OneToOneField(BaseMember, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(
        upload_to='staff_profile_pics/',
        validators=[FileExtensionValidator(['jpg', 'png'])],
        blank=True
    )

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.full_name} ({self.role})"

# Squad Member Model
class SquadMember(models.Model):
    POSITION_CHOICES = [
        ('Goalkeeper', 'Goalkeeper'),
        ('Defender', 'Defender'),
        ('Midfielder', 'Midfielder'),
        ('Forward', 'Forward'),
    ]
    FOOT_CHOICES = [('L', 'Left'), ('R', 'Right')]

    base_member = models.OneToOneField(BaseMember, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    citizenship = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    strong_foot = models.CharField(max_length=1, choices=FOOT_CHOICES)
    jersey_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    nickname = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(
        upload_to='squad_profile_pics/',
        validators=[FileExtensionValidator(['jpg', 'png'])],
        blank=True
    )
    market_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    team_level = models.CharField(max_length=10, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['team', 'jersey_number'],
                name='unique_jersey_per_team'
            )
        ]

    def clean(self):
        # Validate citizenship
        if not pycountry.countries.get(name=self.citizenship):
            raise ValidationError({'citizenship': 'Invalid country name.'})

    def save(self, *args, **kwargs):
        self.team_level = self._calculate_team_level()
        super().save(*args, **kwargs)

    def _calculate_team_level(self):
        # Age as of January 1st of current year
        today = date.today()
        cutoff_date = date(today.year, 1, 1)
        age = cutoff_date.year - self.dob.year - (
            (cutoff_date.month, cutoff_date.day) < (self.dob.month, self.dob.day)
        )

        if age <= 12: return 'U13'
        elif age <= 14: return 'U15'
        elif age <= 18: return 'U19'
        elif age <= 20: return 'U21'
        else: return 'Senior'

    def __str__(self):
        return f"{self.full_name} ({self.position})"


class NeedsPost(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.team.team_name}"
    

class TeamPhoto(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='team_photos/',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TeamVideo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    youtube_link = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)