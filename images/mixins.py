import time
import uuid

from django.core import signing
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound

from DRF_image_upload_app.settings import DEFAULT_EXPIRING_LINK_TIME, MIN_EXPIRING_LINK_TIME, MAX_EXPIRING_LINK_TIME
from images.models import Image, ExpiringLink


class ExpiringLinkMixin:
    def generate_expiring_link(self, image: Image, expires_in: str = DEFAULT_EXPIRING_LINK_TIME) -> dict:

        user_account_tier = image.user.account_tier
        if not user_account_tier.can_generate_expiring_links:
            raise PermissionDenied("This user cannot generate expiring link.")

        if not expires_in.isdigit() or not MIN_EXPIRING_LINK_TIME <= (expires := int(expires_in)) <= MAX_EXPIRING_LINK_TIME:
            raise ValidationError('Expiring link time should be between %d and %d' % (MIN_EXPIRING_LINK_TIME, MAX_EXPIRING_LINK_TIME))

        pk = uuid.uuid4()
        signed_link = signing.dumps(str(pk))

        url = self.request.build_absolute_uri(reverse('expiring-link-detail', kwargs={'signed_link': signed_link}))

        current_timestamp = int(time.time())
        expiry_time = current_timestamp + expires

        # create expiring link
        ExpiringLink.objects.create(id=pk, link=url, image=image, expires_in=expiry_time)

        return {'link': url}

    @staticmethod
    def decode_signed_value(value: str) -> ExpiringLink.id:
        try:
            return signing.loads(value)
        except signing.BadSignature:
            raise NotFound("Invalid signed link")