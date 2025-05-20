# nsfp_core/validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image_size(value):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError(_("File size must be under 2MB."))