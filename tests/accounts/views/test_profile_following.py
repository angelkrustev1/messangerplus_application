from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

UserModel = get_user_model()


class ProfileFollowingTests(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', email='user1@test.com', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='user2', email='user2@test.com', password='testPass2')
        self.user3 = UserModel.objects.create_user(username='user3', email='user3@test.com', password='testPass3')

        self.user1.profile.following.add(self.user2.profile, self.user3.profile)

        self.client.login(username='user1', password='testPass1')

    def test_profile_following_page_authenticated_user(self):
        response = self.client.get(reverse('profile-following', kwargs={'pk': self.user1.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user3.username)
        self.assertTemplateUsed(response, 'accounts/profile-following-page.html')

    def test_profile_following_page_other_user(self):
        response = self.client.get(reverse('profile-following', kwargs={'pk': self.user2.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'accounts/profile-following-page.html')

    def test_profile_following_search(self):
        response = self.client.get(reverse('profile-following', kwargs={'pk': self.user1.pk}), {'query': 'user2'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user2.username)
        self.assertNotContains(response, self.user3.username)

    def test_profile_following_page_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('profile-following', kwargs={'pk': self.user1.pk}))

        self.assertRedirects(
            response,
            f'/accounts/login/?next={reverse("profile-following", kwargs={"pk": self.user1.pk})}'
        )
