# nsfp_core/validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image_size(value):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError(_("File size must be under 2MB."))

def validate_squad_username(value):
    """PascalCase username validation for squad members"""
    if not re.match(r'^[A-Z][a-zA-Z0-9]{3,29}$', value):
        raise ValidationError(
            "Username must start with uppercase letter, 4-30 characters, letters/numbers only"
        )