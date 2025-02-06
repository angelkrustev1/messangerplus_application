from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


UserModel = get_user_model()


class SearchProfilesPageTests(TestCase):

    def setUp(self):
        self.user1 = UserModel.objects.create_user(username='user1', email='user1@test.com', password='testPass1')
        self.user2 = UserModel.objects.create_user(username='user2', email='user2@test.com', password='testPass2')
        self.user3 = UserModel.objects.create_user(username='user3', email='user3@test.com', password='testPass3')

        self.client.login(username='user1', password='testPass1')

    def test_search_profiles_page_authenticated(self):
        response = self.client.get(reverse('search-profiles'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'common/search-profiles-page.html')

    def test_search_profiles_page_no_query(self):
        response = self.client.get(reverse('search-profiles'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['all_users']), 2)

    def test_search_profiles_page_with_query(self):
        response = self.client.get(reverse('search-profiles'), {'query': 'user2'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['all_users']), 1)

    def test_search_profiles_page_query_no_results(self):
        response = self.client.get(reverse('search-profiles'), {'query': 'nonexistent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['all_users']), 0)

    def test_search_profiles_page_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('search-profiles'))

        self.assertRedirects(response, '/accounts/login/?next=/search-profiles/')
