from django.contrib.auth import get_user_model
from django.test import TestCase

from DRF_image_upload_app.settings import TIERS_CONFIG
from accounts.models import AccountTier


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_user = get_user_model().objects.create(
            username='basic@gmail.com',
            password="secret",
        )
        account_tier = AccountTier.objects.get(name='Basic')
        cls.basic_user.account_tier = account_tier

        cls.premium_user = get_user_model().objects.create(
            username='premium@gmail.com',
            password="secret",
        )
        account_tier = AccountTier.objects.get(name='Premium')
        cls.premium_user.account_tier = account_tier

        cls.enterprise_user = get_user_model().objects.create(
            username='enterprise@gmail.com',
            password="secret",
        )
        account_tier = AccountTier.objects.get(name='Enterprise')
        cls.enterprise_user.account_tier = account_tier

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test_user", email="test_user@email.com", password="cba123jashD"
        )
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test_user@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="admin", email="test_admin@email.com", password="sadhfiuD123"
        )
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "test_admin@email.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_users_accounts_tiers(self):
        self.assertEqual(self.basic_user.account_tier.name, "Basic")
        self.assertEqual(self.premium_user.account_tier.name, "Premium")
        self.assertEqual(self.enterprise_user.account_tier.name, "Enterprise")

    def test_available_thumbnails(self):
        default_thumbnails = [t.get('thumbnail_size') for t in TIERS_CONFIG.values() if t.get('thumbnail_size')]
        basic_tier_account = default_thumbnails[0]
        premium_tier_account = [basic_tier_account, default_thumbnails[1]]
        enterprise_tier_account = premium_tier_account

        current_user_basic = [dict(width=e.width, height=e.height) for e in
                              self.basic_user.account_tier.get_thumbnail_sizes]
        current_user_premium = [dict(width=e.width, height=e.height) for e in
                                self.premium_user.account_tier.get_thumbnail_sizes]
        current_user_enterprise = [dict(width=e.width, height=e.height) for e in
                                   self.enterprise_user.account_tier.get_thumbnail_sizes]

        self.assertEqual(current_user_basic, [basic_tier_account])
        self.assertEqual(current_user_premium, premium_tier_account)
        self.assertEqual(current_user_enterprise, enterprise_tier_account)

    def test_can_generate_expiring_links(self):
        self.assertFalse(self.basic_user.account_tier.can_generate_expiring_links)
        self.assertFalse(self.premium_user.account_tier.can_generate_expiring_links)
        self.assertTrue(self.enterprise_user.account_tier.can_generate_expiring_links)

    def test_can_get_original_file(self):
        self.assertFalse(self.basic_user.account_tier.can_get_original_image)
        self.assertTrue(self.premium_user.account_tier.can_get_original_image)
        self.assertTrue(self.enterprise_user.account_tier.can_get_original_image)

