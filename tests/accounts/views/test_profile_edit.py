import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

UserModel = get_user_model()


class ProfileEditTests(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', email='user1@test.com', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='user2', email='user2@test.com', password='testPass2')
        self.admin_user = UserModel.objects.create_superuser(
            username='supertest',
            email='super@test.com',
            password='superPass123',
        )

        self.client.login(username='user1', password='testPass1')

    def test_profile_edit_page_authenticated_owner(self):
        response = self.client.get(reverse('profile-edit', kwargs={'pk': self.user1.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'accounts/profile-edit-page.html')

    def test_profile_edit_page_authenticated_non_owner(self):
        response = self.client.get(reverse('profile-edit', kwargs={'pk': self.user2.pk}))

        self.assertRedirects(response, reverse('index'))

    def test_profile_edit_page_admin_access(self):
        self.client.login(username='supertest', password='superPass123')
        response = self.client.get(reverse('profile-edit', kwargs={'pk': self.user2.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'accounts/profile-edit-page.html')

    def test_profile_edit_page_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('profile-edit', kwargs={'pk': self.user1.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/accounts/profile/{self.user1.pk}/edit/')

    def test_profile_edit_form_submission_valid(self):
        response = self.client.post(reverse('profile-edit', kwargs={'pk': self.user1.pk}), {
            'biography': 'Updated Bio',
        })

        self.user1.profile.refresh_from_db()
        self.assertEqual(self.user1.profile.biography, 'Updated Bio')
        self.assertRedirects(response, reverse('profile-details', kwargs={'pk': self.user1.pk}))

    def test_profile_edit_form_submission_with_image(self):
        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'no-post-image.png')
        with open(image_path, 'rb') as img_file:
            image = SimpleUploadedFile('test_image.jpg', img_file.read(), content_type='image/png')

        response = self.client.post(reverse('profile-edit', kwargs={'pk': self.user1.pk}), {
            'biography': 'Updated Bio with Image',
            'profile_picture': image,
        })

        self.user1.profile.refresh_from_db()
        self.assertEqual(self.user1.profile.biography, 'Updated Bio with Image')
        self.assertTrue(self.user1.profile.profile_picture)

    def test_profile_edit_form_invalid_submission(self):
        long_biography = 'M' * 251

        response = self.client.post(reverse('profile-edit', kwargs={'pk': self.user1.pk}), {
            'biography': long_biography,
        })

        self.user1.profile.refresh_from_db()
        self.assertNotEqual(self.user1.profile.biography, long_biography)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
