import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from MessangerplusApp.posts.forms import PostCreationForm
from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class CreatePostViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(username='test', email='user@user.com', password='testPass1')
        self.url = reverse('create-post')

        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'no-post-image.png')
        with open(image_path, 'rb') as img_file:
            self.image = SimpleUploadedFile('test_image.jpg', img_file.read(), content_type='image/png')

        self.post_credentials = {
            'user': self.user,
            'photo': self.image,
            'title': 'test post',
        }

    def test_create_post_view_redirect_for_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_create_post_view_get(self):
        self.client.login(username='test', password='testPass1')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'posts/post-create-page.html')
        self.assertIsInstance(response.context['form'], PostCreationForm)

    def test_create_post_view_post_valid_form(self):
        self.client.login(username='test', password='testPass1')
        response = self.client.post(self.url, self.post_credentials)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'test post')
        self.assertEqual(post.user, self.user)

    def test_create_post_view_post_invalid_form(self):
        self.client.login(username='test', password='testPass1')
        self.post_credentials['title'] = ''
        response = self.client.post(self.url, self.post_credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 0)
