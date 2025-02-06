import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from MessangerplusApp.common.models import Like
from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class LikeFunctionalityTests(TestCase):

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

    def test_like_post(self):
        self.client.login(username='test', password='testPass1')

        response = self.client.get(
            reverse('like', kwargs={'post_pk': self.post.pk}),
            HTTP_REFERER=reverse('index')
        )

        self.assertEqual(Like.objects.count(), 1)
        like = Like.objects.first()
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.to_post, self.post)
        self.assertRedirects(response, reverse('index') + f'#{self.post.pk}')

    def test_unlike_post(self):
        self.client.login(username='test', password='testPass1')

        Like.objects.create(user=self.user, to_post=self.post)

        response = self.client.get(
            reverse('like', kwargs={'post_pk': self.post.pk}),
            HTTP_REFERER=reverse('index')
        )

        self.assertEqual(Like.objects.count(), 0)
        self.assertRedirects(response, reverse('index') + f'#{self.post.pk}')

    def test_like_post_as_anonymous_user(self):
        response = self.client.get(reverse('like', kwargs={'post_pk': self.post.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/like/{self.post.pk}/')
