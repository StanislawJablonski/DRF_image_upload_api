import os

from django.core.exceptions import ValidationError

from DRF_image_upload_app.settings import MAX_FILE_SIZE, MAX_EXPIRING_LINK_TIME, MIN_EXPIRING_LINK_TIME


def validate_image_size_extension(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError('Please upload an image below 15MB.')

    extension = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".png"]
    if not extension.lower() in valid_extensions:
        raise ValidationError("Please upload an image in .JPG or .PNG format.")


def validate_expiring_time(value):
    if not MIN_EXPIRING_LINK_TIME <= value <= MAX_EXPIRING_LINK_TIME:
        raise ValidationError(
            f'Expiration time must be between {MIN_EXPIRING_LINK_TIME} and {MAX_EXPIRING_LINK_TIME} seconds.')
