import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class IndexViewTest(TestCase):

    def setUp(self):
        self.user_credentials = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'testPass123',
        }
        self.admin_credentials = {
            'username': 'supertest',
            'email': 'supertest@test.com',
            'password': 'superPass123',
        }
        self.user = UserModel.objects.create_user(**self.user_credentials)
        self.admin_user = UserModel.objects.create_superuser(**self.admin_credentials)

        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'no-post-image.png')
        with open(image_path, 'rb') as img_file:
            self.image = SimpleUploadedFile("test_image.jpg", img_file.read(), content_type="image/png")

        self.post_credentials = {
            'user': self.user,
            'photo': self.image,
            'title': 'test post',
        }
        [Post.objects.create(**self.post_credentials) for _ in range(11)]

    def test_redirect_if_not_authenticated(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'common/no-profile-home-page.html')

    def test_authenticated_user_can_access(self):
        self.client.login(username='test', password='testPass123')
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'common/profile-home-page.html')
        self.assertIn('posts', response.context)

    def test_search_functionality(self):
        self.client.login(username='test', password='testPass123')
        response = self.client.get(reverse('index'), {'query': 'test'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'test post')

    def test_pagination(self):
        self.client.login(username='test', password='testPass123')
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['posts'].has_next())

    def test_admin_user_can_administer_posts(self):
        self.client.login(username='supertest', password='superPass123')
        response = self.client.get(reverse('index'))

        self.assertTrue(response.context['can_administer_posts'])
