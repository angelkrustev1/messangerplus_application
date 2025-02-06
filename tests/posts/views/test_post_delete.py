import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class PostDeleteViewTest(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='test1', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='test2', password='testPass2')
        self.admin_user = UserModel.objects.create_superuser(
            username='supertest',
            email='super@test.com',
            password='superPass123',
        )

        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'no-post-image.png')
        with open(image_path, 'rb') as img_file:
            self.image = SimpleUploadedFile('test_image.jpg', img_file.read(), content_type='image/png')

        self.post_credentials = {
            'user': self.user1,
            'photo': self.image,
            'title': 'test post',
        }
        self.post = Post.objects.create(**self.post_credentials)

        self.url = reverse('post-delete', kwargs={'post_pk': self.post.pk})
        self.client.login(username='test1', password='testPass1')

    def test_post_delete_view_delete_own_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse('profile-details', kwargs={'pk': self.user1.pk})
        )
        self.assertEqual(Post.objects.count(), 0)

    def test_post_delete_view_admin_can_delete_any_post(self):
        self.client.login(username='supertest', password='superPass123')
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse('profile-details', kwargs={'pk': self.user1.pk}))
        self.assertEqual(Post.objects.count(), 0)

    def test_post_delete_view_redirect_if_not_authorized(self):
        self.client.login(username='test2', password='testPass2')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), 1)

    def test_post_delete_view_404_for_non_existent_post(self):
        invalid_url = reverse('post-delete', kwargs={'post_pk': 99999})
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_delete_view_redirect_for_anonymous_user(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
