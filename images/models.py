import os
import time
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models

from images.validators import validate_expiring_time, validate_image_size_extension

User = settings.AUTH_USER_MODEL


class ThumbnailSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f"{self.width}x{self.height}"


def image_upload_path(instance, filename):
    return f"{instance.user.id}/images/{instance.id}/{filename}"


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path, max_length=255, validators=[validate_image_size_extension])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.image}"

    def __repr__(self):
        return """Image(id='%s', user='%s', image='%s', created_at='%s')""" % (
            self.id,
            self.user,
            self.image.name,
            self.created_at,
        )

    @property
    def get_url(self):
        return self.image.url

    def get_thumbnails(self):
        user_account_tier = self.user.account_tier
        available_thumbnail_sizes = user_account_tier.get_dimensions

        base_file = os.path.dirname(self.image.name)
        storage = default_storage

        thumbnails = storage.listdir(base_file)[1]

        thumbnails_to_return = []
        for thumbnail in thumbnails:
            name, _ = thumbnail.rsplit(".", 1)
            height = name.split("_")[-1]

            if height.isdigit() and int(height) in available_thumbnail_sizes:
                path_to_thumbnail = os.path.join(base_file, thumbnail)
                thumbnails_to_return.append(path_to_thumbnail)

        if user_account_tier.can_get_original_image:
            thumbnails_to_return.append(self.get_url)

        if user_account_tier.can_generate_expiring_links and hasattr(self, 'expiring_link'):
            thumbnails_to_return.append(self.expiring_link.link)

        return thumbnails_to_return


class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name="expiring_link", unique=True)
    link = models.CharField(max_length=255)
    expires_in = models.IntegerField(validators=[validate_expiring_time])

    def __str__(self):
        return f"{self.link} - {self.image}"

    def __repr__(self):
        return """ExpiringLink(image='%s', link='%s', expires_in='%s')""" % (self.image, self.link, self.expires_in)

    def is_expired(self):
        current_time = time.time()
        return current_time > self.expires_in
