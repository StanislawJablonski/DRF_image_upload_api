import uuid

from django.conf import settings
from django.db import models

from DRF_image_upload_app.settings import MEDIA_ROOT

User = settings.AUTH_USER_MODEL


class ThumbnailSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f"{self.width}x{self.height}"


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=MEDIA_ROOT, max_length=255)  # add validation
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.image}"


class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name="expiring_link", unique=True)
    link = models.CharField(max_length=255)
    expires_in = models.IntegerField()  # add validation

