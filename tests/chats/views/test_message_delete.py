from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from MessangerplusApp.chats.models import Message

UserModel = get_user_model()


class MessageDeleteTests(TestCase):
    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', email='user1@test.com', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='user2', email='user2@test.com', password='testPass2')
        self.admin_user = UserModel.objects.create_superuser(
            username='supertest',
            email='super@test.com',
            password='superPass123',
        )

        self.message1 = Message.objects.create(sender=self.user1, recipient=self.user2, content='Hello from user1')
        self.message2 = Message.objects.create(sender=self.user2, recipient=self.user1, content='Hello from user2')

    def test_login_required(self):
        response = self.client.post(reverse(
            'message-delete',
            kwargs={'pk': self.user2.pk, 'message_pk': self.message1.pk}
        ))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_user_can_delete_own_message(self):
        self.client.login(username='user1', password='testPass1')

        response = self.client.post(reverse(
            'message-delete',
            kwargs={'pk': self.user2.pk, 'message_pk': self.message1.pk}
        ))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertFalse(Message.objects.filter(pk=self.message1.pk).exists())

    def test_user_cannot_delete_others_messages(self):
        self.client.login(username='user1', password='testPass1')

        response = self.client.post(reverse(
            'message-delete',
            kwargs={'pk': self.user2.pk, 'message_pk': self.message2.pk}
        ))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(Message.objects.filter(pk=self.message2.pk).exists())

    def test_admin_can_delete_any_message(self):
        self.client.login(username='supertest', password='superPass123')

        response = self.client.post(reverse(
            'message-delete',
            kwargs={'pk': self.user2.pk, 'message_pk': self.message1.pk}
        ))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertFalse(Message.objects.filter(pk=self.message1.pk).exists())
