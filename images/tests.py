import os
from io import BytesIO
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import AccountTier
from images.models import ExpiringLink, Image


def create_temporary_image():
    from PIL import Image
    test_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'windows.jpg')
    with open(test_image_path, 'rb') as f:
        image_data = BytesIO(f.read())

    image = Image.open(image_data)
    image_file = BytesIO()
    image.save(image_file, format='JPEG')
    image_file.seek(0)

    return InMemoryUploadedFile(
        image_file,
        None,
        'windows.jpg',
        'image/jpeg',
        image_file.tell,
        None
    )


class ImageModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@email.com',
            password='secret',
            is_staff=True,
            is_active=True,
        )
        cls.image_file = create_temporary_image()
        cls.image = Image.objects.create(
            user=cls.user,
            image=cls.image_file,
        )

        cls.expected_image_name = 'windows'
        cls.expected_ext = '.jpg'
        cls.expected_image_path = cls.image.get_url


    def test_image_owner(self):
        self.assertEqual(self.image.user.username, "test_user")
        self.assertNotEqual(self.image.user.email, 'invalid@email.com')

    def test_image_str_method(self):
        expected_str = f"{str(self.user)} - {self.expected_image_path.rsplit('/media/')[1]}"
        self.assertEqual(str(self.image), expected_str)

    def test_image_repr_method(self):
        expected_repr = f"""Image(id='{self.image.id}', user='{self.user}', image='{self.expected_image_path.rsplit('/media/')[1]}', created_at='{self.image.created_at}')"""
        self.assertEqual(repr(self.image), expected_repr)

    def test_get_url_method(self):
        self.assertEqual(self.image.get_url, self.expected_image_path)


class ImageAPITestCase(APITestCase):
    def setUp(self):
        enterprise_account = AccountTier.objects.get(id=3)
        self.user = get_user_model().objects.create_user(username='test_user', password='testpass',
                                                         account_tier=enterprise_account)
        self.client.login(username='test_user', password='testpass')
        self.image_file = create_temporary_image()

    def test_create_image(self):
        url = reverse('image-create')

        data = {'image': self.image_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Image.objects.first().user, self.user)

    def test_list_images(self):
        Image.objects.create(user=self.user, image=self.image_file)
        url = reverse('image-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_expiring_link(self):
        image = Image.objects.create(user=self.user, image=self.image_file)
        url = reverse('expiring-link-create-list')
        data = {'image': image.id, 'expires_in': '3600'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpiringLink.objects.count(), 1)
        self.assertEqual(Image.objects.first().user, self.user)


    def test_get_expiring_link_detail(self):
        image = Image.objects.create(user=self.user, image=self.image_file)
        url = reverse('expiring-link-create-list')
        data = {'image': image.id, 'expires_in': '3600'}
        response = self.client.post(url, data, format='json')
        link = response.data.get('link').split('/')[-2]
        url = reverse('expiring-link-detail', kwargs={'signed_link': link})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expiring_link_detail_with_expired_link(self):
        image = Image.objects.create(user=self.user, image=self.image_file)
        expiring_link = ExpiringLink.objects.create(image=image, link='abc', expires_in=-3600)
        url = reverse('expiring-link-detail', kwargs={'signed_link': expiring_link.link})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
