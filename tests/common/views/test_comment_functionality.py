import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from MessangerplusApp.common.models import Comment
from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class CommentFunctionalityTests(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(username='test', password='testPass1')

        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'no-post-image.png')
        with open(image_path, 'rb') as img_file:
            self.image = SimpleUploadedFile("test_image.jpg", img_file.read(), content_type='image/png')

        self.post_credentials = {
            'user': self.user,
            'photo': self.image,
            'title': 'test post',
        }
        self.post = Post.objects.create(**self.post_credentials)

    def test_comment_creation_with_valid_form(self):
        self.client.login(username='test', password='testPass1')

        data = {'content': 'This is a test comment.'}
        response = self.client.post(reverse('comment', kwargs={'post_pk': self.post.pk}), data)

        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.to_post, self.post)

        self.assertRedirects(response, reverse('post-details', kwargs={'post_pk': self.post.pk}))

    def test_comment_creation_for_logged_out_user(self):
        data = {'content': 'This comment should not be posted.'}
        response = self.client.post(reverse('comment', kwargs={'post_pk': self.post.pk}), data)

        self.assertRedirects(response, f'/accounts/login/?next=/comment/{self.post.pk}/')

    def test_comment_creation_with_invalid_form(self):
        self.client.login(username='test', password='testPass1')

        data = {'content': ''}
        response = self.client.post(reverse('comment', kwargs={'post_pk': self.post.pk}), data)

        self.assertEqual(Comment.objects.count(), 0)
        self.assertRedirects(response, reverse('post-details', kwargs={'post_pk': self.post.pk}))

    def test_comment_redirection_for_non_logged_in_user(self):
        response = self.client.get(reverse('comment', kwargs={'post_pk': self.post.pk}))
        self.assertRedirects(response, f'/accounts/login/?next=/comment/{self.post.pk}/')
