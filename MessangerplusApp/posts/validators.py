from django.core.exceptions import ValidationError


def validate_picture_size(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError('The pictures exceeds the limit of 5MB')
