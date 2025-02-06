from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class FollowFunctionalityTests(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='test1', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='test2', password='testPass2')

        self.client.login(username='test1', password='testPass1')

    def test_follow_user(self):
        response = self.client.get(
            reverse('follow', kwargs={'user_pk': self.user2.pk}),
            HTTP_REFERER=reverse('search-profiles')
        )

        self.assertIn(self.user2.profile, self.user1.profile.following.all())
        self.assertRedirects(response, reverse('search-profiles') + f'#{self.user2.pk}')

    def test_unfollow_user(self):
        self.user1.profile.following.add(self.user2.profile)

        response = self.client.get(
            reverse('follow', kwargs={'user_pk': self.user2.pk}),
            HTTP_REFERER=reverse('search-profiles')
        )

        self.assertNotIn(self.user2.profile, self.user1.profile.following.all())
        self.assertRedirects(response, reverse('search-profiles') + f'#{self.user2.pk}')

    def test_follow_self(self):
        response = self.client.get(
            reverse('follow', kwargs={'user_pk': self.user1.pk}),
            HTTP_REFERER=reverse('search-profiles')
        )

        self.assertNotIn(self.user1.profile, self.user1.profile.following.all())

    def test_follow_user_as_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('follow', kwargs={'user_pk': self.user2.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/follow/{self.user2.pk}/')
