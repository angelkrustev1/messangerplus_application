import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from MessangerplusApp.posts.forms import PostEditForm
from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class PostEditViewTest(TestCase):

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

        self.url = reverse('post-edit', kwargs={'post_pk': self.post.pk})
        self.client.login(username='test1', password='testPass1')

    def test_post_edit_view_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'posts/post-edit-page.html')
        self.assertEqual(response.context['post'], self.post)
        self.assertIsInstance(response.context['form'], PostEditForm)

    def test_post_edit_view_post_valid_form(self):
        self.post_credentials['title'] = 'new title'
        response = self.client.post(self.url, self.post_credentials)

        self.assertRedirects(
            response,
            reverse('post-details', kwargs={'post_pk': self.post.pk})
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'new title')

    def test_post_edit_view_invalid_form(self):
        self.post_credentials['title'] = ''
        response = self.client.post(self.url, self.post_credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.title, 'test post')

    def test_post_edit_view_accessed_by_admin(self):
        self.client.login(username='supertest', password='superPass123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'posts/post-edit-page.html')
        self.assertEqual(response.context['post'], self.post)
        self.assertIsInstance(response.context['form'], PostEditForm)

    def test_post_edit_not_owner_or_admin_access_rejected(self):
        self.client.login(username='test2', password='testPass2')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_post_edit_view_redirect_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
