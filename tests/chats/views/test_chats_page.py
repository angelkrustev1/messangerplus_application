from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

UserModel = get_user_model()


class ChatsPageTests(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', email='user1@test.com', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='user2', email='user2@test.com', password='testPass2')
        self.user3 = UserModel.objects.create_user(username='user3', email='user3@test.com', password='testPass3')

        self.user1.profile.following.add(self.user2.profile)
        self.user2.profile.following.add(self.user1.profile)

        self.user1.profile.following.add(self.user3.profile)

        self.client.login(username='user1', password='testPass1')

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('chats'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_mutual_followers_displayed(self):
        response = self.client.get(reverse('chats'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'user2')
        self.assertNotContains(response, 'user3')
        self.assertTemplateUsed(response, 'chats/all-chats-page.html')

    def test_search_functionality(self):
        response = self.client.get(reverse('chats'), {'query': 'user2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2.profile, response.context['mutual_followers'])
        self.assertNotIn(self.user3.profile, response.context['mutual_followers'])

        response = self.client.get(reverse('chats'), {'query': 'user3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user2.profile, response.context['mutual_followers'])
        self.assertNotIn(self.user3.profile, response.context['mutual_followers'])

    def test_empty_search_returns_all_mutual_followers(self):
        response = self.client.get(reverse('chats'), {'query': ''})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'user2')
