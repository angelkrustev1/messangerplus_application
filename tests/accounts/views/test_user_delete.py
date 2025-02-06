from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserDeleteTests(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', email='user1@test.com', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='user2', email='user2@test.com', password='testPass2')
        self.admin_user = UserModel.objects.create_superuser(
            username='supertest',
            email='super@test.com',
            password='superPass123',
        )

        self.client.login(username='user1', password='testPass1')

    def test_user_delete_own_account(self):
        response = self.client.post(reverse('user-delete', kwargs={'pk': self.user1.pk}))

        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(pk=self.user1.pk)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('index'))

    def test_user_delete_another_user_without_permission(self):
        response = self.client.post(reverse('user-delete', kwargs={'pk': self.user2.pk}))

        self.assertTrue(UserModel.objects.filter(pk=self.user2.pk).exists())
        self.assertRedirects(response, reverse('index'))

    def test_admin_can_delete_any_user(self):
        self.client.login(username='supertest', password='superPass123')
        response = self.client.post(reverse('user-delete', kwargs={'pk': self.user2.pk}))

        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(pk=self.user2.pk)

        self.assertRedirects(response, reverse('index'))

    def test_unauthenticated_user_redirected(self):
        self.client.logout()
        response = self.client.post(reverse('user-delete', kwargs={'pk': self.user1.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/accounts/user/{self.user1.pk}/delete')
