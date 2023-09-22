from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from DRF_image_upload_app.settings import TIERS_CONFIG
from accounts.models import AccountTier, User
from images.models import ThumbnailSize


@receiver(post_migrate)
def create_default_account_tiers(sender, **kwargs):
    if sender.name == User._meta.app_label:
        if AccountTier.objects.filter(name="Basic").exists():
            return

        basic_tier = AccountTier.objects.create(
            name="Basic",
            can_get_original_image=TIERS_CONFIG['BASIC']['can_get_original_image'],
            can_generate_expiring_links=TIERS_CONFIG['BASIC']['can_generate_expiring_links'],
        )
        basic_thumbnail = ThumbnailSize.objects.create(**TIERS_CONFIG['BASIC']['thumbnail_size'])
        basic_tier.thumbnail_sizes.add(basic_thumbnail)

        premium_tier = AccountTier.objects.create(
            name="Premium",
            can_get_original_image=TIERS_CONFIG['PREMIUM']['can_get_original_image'],
            can_generate_expiring_links=TIERS_CONFIG['PREMIUM']['can_generate_expiring_links'],
        )
        premium_thumbnail = ThumbnailSize.objects.create(**TIERS_CONFIG['PREMIUM']['thumbnail_size'])
        premium_tier.thumbnail_sizes.set([basic_thumbnail, premium_thumbnail])

        enterprise_tier = AccountTier.objects.create(
            name="Enterprise",
            can_get_original_image=TIERS_CONFIG['ENTERPRISE']['can_get_original_image'],
            can_generate_expiring_links=TIERS_CONFIG['ENTERPRISE']['can_generate_expiring_links'],
        )
        enterprise_tier.thumbnail_sizes.set([basic_thumbnail, premium_thumbnail])


@receiver(post_save, sender=User)
def create_user_account(instance, created, **kwargs):
    if created and not instance.account_tier:
        instance.account_tier = AccountTier.objects.get(name="Basic")
        instance.save()
