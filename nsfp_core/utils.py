# core/utils.py
import re
from django.core.exceptions import ValidationError
from datetime import date

SUFFIXES = {'fc', 'cf', 'club', 'team', 'sc', 'united', 'city', 'afc'}

def normalize_identifier(name):
    """
    Universal normalization that:
    1. Removes ALL non-alphabetic characters
    2. Removes ALL suffixes (anywhere in string)
    3. Converts to PascalCase
    """
    # Remove all non-letters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z]', '', name).lower()
    
    # Remove ALL suffix occurrences (not just trailing)
    for suffix in SUFFIXES:
        cleaned = cleaned.replace(suffix, '')
    
    # Convert to PascalCase (capitalize first letter)
    return cleaned.capitalize() if cleaned else 'Team'

def validate_team_name(name):
    """Validate team name meets display requirements"""
    if not re.match(r'^[A-Z][a-zA-Z ]+[a-zA-Z]$', name):
        raise ValidationError(
            "Team name must:\n"
            "1. Start with capital letter\n"
            "2. Contain only letters and spaces\n"
            "3. Have proper English capitalization\n"
            "Examples: 'Chelsea', 'Real Madrid', 'PSG'"
        )
    
    # Check if name is just suffix(es)
    words = [word.lower() for word in name.split()]
    if all(word in SUFFIXES for word in words):
        raise ValidationError(
            "Team name cannot be just suffixes (like 'FC' or 'City United')"
        )

def validate_username(name):
    """Validate username meets requirements"""
    if not re.match(r'^[A-Z][a-zA-Z]+$', name):
        raise ValidationError(
            "Username must:\n"
            "1. Start with capital letter\n"
            "2. Contain only letters (no numbers/symbols)\n"
            "3. Example: 'Chelsea', 'KaizerChiefs'"
        )
    



def calculate_team_level(dob):
    today = date.today()
    cutoff_date = date(today.year, 1, 1)
    age = cutoff_date.year - dob.year - (
        (cutoff_date.month, cutoff_date.day) < (dob.month, dob.day)
    )
    
    if age <= 13:
        return 'U13'
    elif age <= 15:
        return 'U15'
    elif age <= 19:
        return 'U19'
    elif age <= 21:
        return 'U21'
    else:
        return 'SR'