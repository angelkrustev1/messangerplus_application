import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from MessangerplusApp.common.models import Comment
from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class CommentDeleteTests(TestCase):

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
            self.image = SimpleUploadedFile('test_image.jpg', img_file.read(), content_type='image/png')

        self.post_credentials = {
            'user': self.user1,
            'photo': self.image,
            'title': 'test post',
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.comment = Comment.objects.create(content='Test comment', user=self.user1, to_post=self.post)

    def test_comment_deletion_by_owner(self):
        self.client.login(username='user1', password='testPass1')

        response = self.client.get(
            reverse('comment-delete', kwargs={'post_pk': self.post.pk, 'comment_pk': self.comment.pk})
        )

        self.assertEqual(Comment.objects.count(), 0)
        self.assertRedirects(response, reverse('post-details', kwargs={'post_pk': self.post.pk}))

    def test_comment_deletion_by_admin(self):
        self.client.login(username='supertest', password='superPass123')

        response = self.client.get(
            reverse('comment-delete', kwargs={'post_pk': self.post.pk, 'comment_pk': self.comment.pk})
        )

        self.assertEqual(Comment.objects.count(), 0)
        self.assertRedirects(response, reverse('post-details', kwargs={'post_pk': self.post.pk}))

    def test_comment_deletion_by_unauthorized_user(self):
        self.client.login(username='user2', password='testPass2')

        response = self.client.get(
            reverse('comment-delete', kwargs={'post_pk': self.post.pk, 'comment_pk': self.comment.pk})
        )

        self.assertEqual(Comment.objects.count(), 1)
        self.assertRedirects(response, reverse('index'))

    def test_comment_deletion_without_login(self):
        response = self.client.get(
            reverse('comment-delete', kwargs={'post_pk': self.post.pk, 'comment_pk': self.comment.pk})
        )

        self.assertRedirects(response, f'/posts/post/{self.post.pk}/')
