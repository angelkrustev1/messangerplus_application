from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from MessangerplusApp.chats.models import Message

UserModel = get_user_model()


class ChatOneOnOneTests(TestCase):

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
        response = self.client.get(reverse('chat-one-on-one', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_denied_if_not_mutual_followers(self):
        response = self.client.get(reverse('chat-one-on-one', kwargs={'pk': self.user3.pk}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_granted_for_mutual_followers(self):
        response = self.client.get(reverse('chat-one-on-one', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'user2')

    def test_send_message(self):
        response = self.client.post(reverse('chat-one-on-one', kwargs={'pk': self.user2.pk}), {
            'content': 'Hello, user2!'
        }, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        message_qr = Message.objects.filter(
            sender=self.user1, recipient=self.user2, content='Hello, user2!'
        )
        self.assertTrue(message_qr.exists(), 'Message was not saved in the database')

        self.assertIn(message_qr.first(), response.context['shared_messages'])

    def test_messages_are_displayed(self):
        Message.objects.create(sender=self.user1, recipient=self.user2, content='Test message')

        response = self.client.get(reverse('chat-one-on-one', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test message')
