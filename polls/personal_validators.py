from django.core.exceptions import ValidationError

def validate_only_letters(value):
    if "sag" in value:
        return value
    else:
        raise ValidationError("just sag")