import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class ProfileDetailsTests(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', email='user1@test.com', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='user2', email='user2@test.com', password='testPass2')
        self.admin_user = UserModel.objects.create_superuser(
            username='supertest',
            email='super@test.com',
            password='superPass123',
        )

        self.client.login(username='user1', password='testPass1')

        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'no-post-image.png')
        with open(image_path, 'rb') as img_file:
            self.image = SimpleUploadedFile("test_image.jpg", img_file.read(), content_type="image/png")

        self.post_credentials = {
            'user': self.user2,
            'photo': self.image,
            'title': 'test post',
        }
        [Post.objects.create(**self.post_credentials) for _ in range(11)]

    def test_profile_details_page_authenticated(self):
        response = self.client.get(reverse('profile-details', kwargs={'pk': self.user2.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user2.username)
        self.assertTemplateUsed(response, 'accounts/profile-details-page.html')

    def test_profile_details_page_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('profile-details', kwargs={'pk': self.user2.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/accounts/profile/{self.user2.pk}/')

    def test_profile_details_page_with_posts(self):
        response = self.client.get(reverse('profile-details', kwargs={'pk': self.user2.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['posts']), 10)

    def test_profile_details_page_pagination(self):
        response = self.client.get(reverse('profile-details', kwargs={'pk': self.user2.pk}), {'page': 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['posts']), 1)

    def test_profile_details_page_can_administer_profiles_permission(self):
        self.client.login(username='supertest', password='superPass123')

        response = self.client.get(reverse('profile-details', kwargs={'pk': self.user2.pk}))

        self.assertTrue(response.context['can_administer_profiles'])

    def test_profile_details_page_no_admin_permission(self):
        response = self.client.get(reverse('profile-details', kwargs={'pk': self.user2.pk}))

        self.assertFalse(response.context['can_administer_profiles'])
