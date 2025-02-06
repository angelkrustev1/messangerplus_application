import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from MessangerplusApp.common.models import Comment
from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class PostDetailsViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(username='test', password='testPass1')
        self.admin_user = UserModel.objects.create_superuser(
            username='supertest',
            email='super@test.com',
            password='superPass123',
        )

        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'no-post-image.png')
        with open(image_path, 'rb') as img_file:
            self.image = SimpleUploadedFile('test_image.jpg', img_file.read(), content_type='image/png')

        self.post_credentials = {
            'user': self.user,
            'photo': self.image,
            'title': 'test post',
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.comment = Comment.objects.create(content='Test comment', to_post=self.post, user=self.user)

        self.url = reverse('post-details', kwargs={'post_pk': self.post.pk})
        self.client.login(username='test', password='testPass1')

    def test_post_details_view_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'posts/post-details-page.html')
        self.assertEqual(response.context['post'], self.post)
        self.assertEqual(len(response.context['comments']), 1)
        self.assertEqual(response.context['comments'][0], self.comment)
        self.assertTrue(response.context['is_details'])

    def test_post_details_view_404_for_non_existent_post(self):
        invalid_url = reverse('post-details', kwargs={'post_pk': 99999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_details_view_user_with_permissions(self):
        self.client.login(username='supertest', password='superPass123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context['can_administer_posts'])
        self.assertTrue(response.context['can_administer_comments'])

    def test_post_details_view_user_without_permissions(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.context['can_administer_posts'])
        self.assertFalse(response.context['can_administer_comments'])

    def test_post_details_view_redirect_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
