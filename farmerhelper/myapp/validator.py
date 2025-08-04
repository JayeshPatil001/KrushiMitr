from django.core.exceptions import ValidationError
import re

def validate_only_letters(value):
    if not re.match(r'^[A-Za-z\s]+$', value):
        raise ValidationError("This field accepts only English letters (A–Z, a–z) and spaces.")
